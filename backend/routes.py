import ast
import base64
import csv
from datetime import datetime
import io
from flask import current_app
from flask import Blueprint, request, jsonify, send_file
from sqlalchemy import extract, func
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from extensions import cache


# JWT Secret Key (Change this for production!)
jwt = JWTManager()
SECRET_KEY = "ShreyaKhantal:)"

route = Blueprint('main', __name__)



# ---------------------- USER AUTHENTICATION ----------------------

@route.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")
    qualification = data.get("qualification")
    dob = data.get("dob")

    if not all([username, email, password, qualification, dob]):
        return jsonify({"message": "All fields are required!"}), 400

    dob = datetime.strptime(dob, "%Y-%m-%d").date()

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered!"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        full_name=full_name,
        qualification=qualification,
        dob=dob,
        role="user",
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201


@route.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    user.last_login = datetime.utcnow()
    db.session.commit()

    # Convert identity to a string (JSON string)
    identity = {"id": user.id, "role": user.role}
    
    access_token = create_access_token(
        identity=str(identity),  # Convert dict to string
        expires_delta=timedelta(hours=1)
    )
    refresh_token = create_refresh_token(identity=str(identity))  # Convert dict to string

    return jsonify(
        {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            'role': user.role,
        }
    ), 200

# Refresh Token (Optional)
@route.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": new_access_token})

#logout
@route.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        # Debugging
        # user_identity = get_jwt_identity()
        # print("User Identity:", user_identity) 
        return jsonify({"message": "Logged out successfully!"}), 200
    except Exception as e:
        print("Error:", str(e))  # Log error
        return jsonify({"error": str(e)}), 401

@route.route("/user-info", methods=["GET"])
@jwt_required()
def user_info():
    identity = get_jwt_identity()  
    user_data = eval(identity) 

    user = User.query.get(user_data["id"])  
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 200


# ---------------------- QUIZ MANAGEMENT (Admin Only) ----------------------

# Middleware: Check if the user is an admin
def admin_required(func):
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        user_data = eval(identity)  # Convert string to dictionary
        user = User.query.get(user_data["id"])

        if not user or user.role != "admin":
            return jsonify({"error": "Access denied! Admins only."}), 403

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return jwt_required()(wrapper)


# Create Subject
@route.route("/admin/create-subject", methods=["POST"])
@admin_required
def create_subject():
    data = request.json
    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"error": "Subject name is required"}), 400

    new_subject = Subject(name=name, description=description)
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({"message": "Subject created successfully!"}), 201

@route.route("/admin/update-subject/<int:subject_id>", methods=["PUT"])
@admin_required
def update_subject(subject_id):
    data = request.json
    name = data.get("name")
    description = data.get("description")

    # Find subject by ID
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    # Update only provided fields
    if name:
        subject.name = name
    if description is not None:  # Allow empty description
        subject.description = description

    db.session.commit()
    return jsonify({"message": "Subject updated successfully!"}), 200

# Create Chapter under a Subject
@route.route("/admin/create-chapter", methods=["POST"])
@admin_required
def create_chapter():
    data = request.json
    subject_id = data.get("subject_id")
    name = data.get("name")
    description = data.get("description")

    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
    db.session.add(new_chapter)
    db.session.commit()
    return jsonify({"message": "Chapter added successfully!"}), 201

@route.route("/admin/update-chapter/<int:chapter_id>", methods=["PUT"])
@admin_required
def update_chapter(chapter_id):
    data = request.json
    name = data.get("name")
    description = data.get("description")
    subject_id = data.get("subject_id")  # Optional: Move chapter to a different subject

    # Find chapter by ID
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({"error": "Chapter not found"}), 404

    # If subject_id is provided, check if the new subject exists
    if subject_id:
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({"error": "New subject not found"}), 404
        chapter.subject_id = subject_id

    # Update only provided fields
    if name:
        chapter.name = name
    if description is not None:  # Allow empty description
        chapter.description = description

    db.session.commit()
    return jsonify({"message": "Chapter updated successfully!"}), 200


# Create Quiz under a Chapter
@route.route("/admin/create-quiz", methods=["POST"])
@admin_required
def create_quiz():
    data = request.json
    chapter_id = data.get("chapter_id")
    title = data.get("title")
    date = data.get("date")  # Expected format: YYYY-MM-DD
    time = data.get("time")  # Expected format: HH:MM
    duration = data.get("duration")  # Duration in minutes
    remarks = data.get("remarks", None)  # Optional field

    # Validate chapter existence
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({"error": "Chapter not found"}), 404

    # Validate required fields
    if not title or not date or not time or duration is None:
        return jsonify({"error": "Missing required fields"}), 400

    # Convert date & time to proper formats if needed
    try:
        from datetime import datetime
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time, "%H:%M").time()
        hours = duration // 60
        minutes = duration % 60
        duration1 = f"{hours:02}:{minutes:02}"
    except ValueError:
        return jsonify({"error": "Invalid date or time format"}), 400
    
    # Create new quiz object
    new_quiz = Quiz(
        title=title,
        chapter_id=chapter_id,
        date_of_quiz=date_obj,
        time_of_quiz=time_obj,
        time_duration=duration1,
        remarks=remarks
    )

    db.session.add(new_quiz)
    db.session.commit()

    return jsonify({"message": "Quiz created successfully!"}), 201

@route.route("/admin/update-quiz/<int:quiz_id>", methods=["PUT"])
@admin_required
def update_quiz(quiz_id):
    data = request.json
    title = data.get("title")
    date = data.get("date")  # Expected format: YYYY-MM-DD
    time = data.get("time")  # Expected format: HH:MM
    duration = data.get("duration")
    remarks = data.get("remarks")

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    # Update fields if provided
    if title:
        quiz.title = title
    if date:
        try:
            from datetime import datetime
            quiz.date_of_quiz = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
    if time:
        try:
            quiz.time_of_quiz = datetime.strptime(time, "%H:%M").time()
        except ValueError:
            return jsonify({"error": "Invalid time format"}), 400
    if duration is not None:
        quiz.time_duration = duration
    if remarks is not None:
        quiz.remarks = remarks

    db.session.commit()
    return jsonify({"message": "Quiz updated successfully!"}), 200

# Fetch all Subjects
@route.route("/admin/get-subjects", methods=["GET"])
@admin_required
def get_subjects():
    subjects = Subject.query.all()
    subject_list = [{"id": subj.id, "name": subj.name, "description": subj.description} for subj in subjects]
    return jsonify(subject_list), 200


# Fetch Chapters under a Subject
@route.route("/admin/get-chapters/<int:subject_id>", methods=["GET"])
@admin_required
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    chapter_list = [{"id": chap.id, "name": chap.name, "description": chap.description, "subject_id": chap.subject_id} for chap in chapters]
    return jsonify(chapter_list), 200

# Fetch Quizzes under a Chapter
@route.route("/admin/get-quizzes/<int:chapter_id>", methods=["GET"])
@admin_required
def get_quizzes(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    quiz_list = [
        {
            "id": quiz.id,
            "title": quiz.title,
            "chapter_id": quiz.chapter_id,
            "date": quiz.date_of_quiz.strftime("%Y-%m-%d") if quiz.date_of_quiz else None,
            "time": quiz.time_of_quiz.strftime("%H:%M") if quiz.time_of_quiz else None,
            "duration": quiz.time_duration,
            "remarks": quiz.remarks
        }
        for quiz in quizzes
    ]
    
    return jsonify(quiz_list), 200

@route.route("/admin/delete-subject/<int:subject_id>", methods=["DELETE"])
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    chapter_ids = [chapter.id for chapter in chapters]
    quizzes = Quiz.query.filter(Quiz.chapter_id.in_(chapter_ids)).all()
    for quiz in quizzes:
        db.session.delete(quiz)
    for chapter in chapters:
        db.session.delete(chapter)
    db.session.delete(subject)
    db.session.commit()

    return jsonify({"message": "Subject and all its chapters and quizzes deleted successfully!"}), 200

# Delete Chapter (Cascades to delete its Quizzes)
@route.route("/admin/delete-chapter/<int:chapter_id>", methods=["DELETE"])
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({"error": "Chapter not found"}), 404

    db.session.delete(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter deleted successfully!"}), 200

# Delete Quiz
@route.route("/admin/delete-quiz/<int:quiz_id>", methods=["DELETE"])
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"message": "Quiz deleted successfully!"}), 200

@route.route("/admin/save-questions/<int:quiz_id>", methods=["POST"])
@admin_required
def save_questions(quiz_id):
    data = request.json  # Get list of questions

    if not isinstance(data, list) or len(data) == 0:
        return jsonify({"error": "Invalid or empty question data"}), 400

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    # ❌ Step 1: Delete all existing questions for this quiz
    Question.query.filter_by(quiz_id=quiz_id).delete()
    db.session.commit()  # Ensure changes are saved before adding new questions

    # Step 2: Add new questions
    new_questions = []
    for q in data:
        question_statement = q.get("text")
        options = q.get("options")
        correct_option = q.get("correct_option")

        if not question_statement or not options or correct_option is None:
            continue  # Skip invalid questions

        if len(options) < 2:
            continue  # Skip if less than two options

        new_question = Question(
            quiz_id=quiz_id,
            question_statement=question_statement,
            options=options,
            correct_option=correct_option
        )
        new_questions.append(new_question)

    # Bulk insert new questions
    db.session.add_all(new_questions)
    db.session.commit()

    return jsonify({"message": "Questions saved successfully!"}), 201

@route.route("/admin/get-questions/<int:quiz_id>", methods=["GET"])
@admin_required
def get_questions(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    question_list = []
    for q in questions:
        question_list.append({
            "id": q.id,
            "text": q.question_statement,
            "options": q.options,
            "correct_option": q.correct_option
        })

    return jsonify(question_list), 200

@route.route("/admin/delete-question/<int:question_id>", methods=["DELETE"])
@admin_required
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify({"message": "Question deleted successfully!"}), 200


# ---------------------- QUIZ ATTEMPT & SCORING (Users) ----------------------
# Middleware: Check if the user is a regular user
def user_required(func):
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        user_data = eval(identity)  # Convert string to dictionary
        user = User.query.get(user_data["id"])

        if not user or user.role != "user":  
            return jsonify({"error": "Access denied! Users only."}), 403  

        return func(*args, **kwargs)  

    wrapper.__name__ = func.__name__  
    return jwt_required()(wrapper)

@route.route("/user/get-subjects", methods=["GET"])
@user_required
def get_all_subjects():
    subjects = Subject.query.all()
    subject_list = [{"id": subj.id, "name": subj.name, "description": subj.description} for subj in subjects]
    return jsonify(subject_list), 200

# Get User Profile
@route.route("/user/profile", methods=["GET"])
@user_required
def get_user_profile():
    identity = get_jwt_identity()
    user_data = eval(identity)
    user = User.query.get(user_data["id"])
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    profile = {
        "id": user.id,
        "name": user.full_name,
        "email": user.email,
        "username": user.username,
        "qualification": user.qualification,
        "dob": user.dob.strftime('%Y-%m-%d') if user.dob else None
    }
    
    return jsonify(profile), 200

# Update User Profile
@route.route("/user/profile", methods=["PUT"])
@user_required
def update_user_profile():
    identity = get_jwt_identity()
    user_data = eval(identity)
    user = User.query.get(user_data["id"])
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    data = request.json
    
    # Update allowed fields
    if "name" in data:
        user.full_name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "phone" in data:
        user.phone = data["phone"]
    
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200


# Get chapters for a subject
@route.route("/user/subject/<int:subject_id>/chapters", methods=["GET"])
@user_required
def get_subject_chapters(subject_id):
    identity = get_jwt_identity()
    user_data = eval(identity)
    user = User.query.get(user_data["id"])

    if not user:
        return jsonify({"error": "User not found"}), 404
        
    # Check if user is enrolled in this subject
    # enrollment = Enrollment.query.filter_by(user_id=user.id, subject_id=subject_id).first()
    # if not enrollment:
    #     return jsonify({"error": "You are not enrolled in this subject"}), 403
        
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    chapter_list = []
    
    for chapter in chapters:
        quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
        total_quizzes = len(quizzes)
        completed_quizzes = 0
        
        for quiz in quizzes:
            score = Score.query.filter_by(user_id=user.id, quiz_id=quiz.id).first()
            if score:
                completed_quizzes += 1
                
        completion = 0
        if total_quizzes > 0:
            completion = int((completed_quizzes / total_quizzes) * 100)
            
        chapter_list.append({
            "id": chapter.id,
            "name": chapter.name,
            "subject_id": chapter.subject_id,
            "description": chapter.description,
            "completion": completion,
            "completed": completion == 100,
            "total_quizzes": total_quizzes,
            "completed_quizzes": completed_quizzes
        })
    
    return jsonify(chapter_list), 200

@route.route("/user/quizzes", methods=["GET"])
@user_required
def get_user_quizzes():
    identity = get_jwt_identity()
    user_data = eval(identity)
    user = User.query.get(user_data["id"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Get all available chapters (no enrollment check)
    chapters = Chapter.query.all()
    chapter_ids = [c.id for c in chapters]

    # Get all quizzes for those chapters
    quizzes = Quiz.query.filter(Quiz.chapter_id.in_(chapter_ids)).all()

    quiz_list = []
    for quiz in quizzes:
        # Check if user has attempted this quiz
        score = Score.query.filter_by(user_id=user.id, quiz_id=quiz.id).first()

        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)

        quiz_data = {
            "id": quiz.id,
            "title": quiz.title,
            "subject": subject.name,
            "chapter": chapter.name,
            "date": quiz.date_of_quiz.strftime('%Y-%m-%d'),
            "time": quiz.time_of_quiz.strftime('%H:%M'),
            "duration": quiz.time_duration,
            "completed": score is not None,
            "score": score.total_scored if score else None,
            "timestamp": score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M') if score else None
        }

        quiz_list.append(quiz_data)

    return jsonify(quiz_list), 200

# Attempt Quiz
@route.route("/user/attempt-quiz/<int:quiz_id>", methods=["POST"])
@user_required
def attempt_quiz(quiz_id):
    identity = get_jwt_identity()
    user_data = eval(identity)
    user_id = user_data["id"]
    
    data = request.json
    total_scored = data.get("total_scored")

    # Check if quiz has already been attempted
    existing_attempt = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
    if existing_attempt:
        return jsonify({"error": "You have already attempted this quiz"}), 400

    new_score = Score(user_id=user_id, quiz_id=quiz_id, total_scored=total_scored)
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"message": "Quiz attempt recorded!", "score": total_scored}), 201

# Get User Scores and Progress
@route.route("/user/progress", methods=["GET"])
@user_required
def get_user_progress():
    identity = get_jwt_identity()
    user_data = eval(identity)
    user_id = user_data["id"]
    
    # Get timeframe from query params (default to 'month')
    timeframe = request.args.get('timeframe', 'month')
    
    # Calculate date threshold based on timeframe
    now = datetime.utcnow()
    if timeframe == 'week':
        # Scores from the last 7 days
        from datetime import timedelta
        date_threshold = now - timedelta(days=7)
    elif timeframe == 'month':
        # Scores from the last 30 days
        from datetime import timedelta
        date_threshold = now - timedelta(days=30)
    elif timeframe == 'year':
        # Scores from the last year
        from datetime import timedelta
        date_threshold = now - timedelta(days=365)
    else:
        # All scores
        date_threshold = datetime(1970, 1, 1)
    
    # Get scores within the timeframe
    scores = Score.query.filter(
        Score.user_id == user_id,
        Score.time_stamp_of_attempt >= date_threshold
    ).order_by(Score.time_stamp_of_attempt).all()
    
    # Process scores
    processed_scores = []
    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)
        
        processed_scores.append({
            "quiz_id": score.quiz_id,
            "quiz_title": quiz.title,
            "subject": subject.name,
            "chapter": chapter.name,
            "timestamp": score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M'),
            "score": score.total_scored,
            "date": score.time_stamp_of_attempt.strftime('%Y-%m-%d')
        })
    
    # Calculate statistics
    total_quizzes = len(processed_scores)
    avg_score = 0
    if total_quizzes > 0:
        avg_score = sum(s["score"] for s in processed_scores) / total_quizzes
    
    # Get subject performance
    subject_performance = {}
    for score in processed_scores:
        subject = score["subject"]
        if subject not in subject_performance:
            subject_performance[subject] = {
                "total_score": 0,
                "count": 0
            }
        subject_performance[subject]["total_score"] += score["score"]
        subject_performance[subject]["count"] += 1
    
    # Calculate average score per subject
    for subject in subject_performance:
        subject_performance[subject]["average"] = subject_performance[subject]["total_score"] / subject_performance[subject]["count"]
    
    # Find strengths and weaknesses
    strengths = []
    weaknesses = []
    
    # Sort subjects by average score
    sorted_subjects = sorted(
        subject_performance.items(),
        key=lambda x: x[1]["average"],
        reverse=True
    )
    
    # Top 3 subjects are strengths
    for subject, data in sorted_subjects[:3]:
        if data["average"] >= 70:  # Only consider as strength if average is at least 70%
            strengths.append(f"Strong performance in {subject} ({data['average']:.1f}%)")
    
    # Bottom 3 subjects are weaknesses
    for subject, data in sorted_subjects[-3:]:
        if data["average"] < 70:  # Only consider as weakness if average is below 70%
            weaknesses.append(f"Need improvement in {subject} ({data['average']:.1f}%)")
    
    return jsonify({
        "scores": processed_scores,
        "statistics": {
            "total_quizzes": total_quizzes,
            "average_score": avg_score,
            "subject_performance": subject_performance
        },
        "strengths": strengths,
        "weaknesses": weaknesses
    }), 200

# Update notification settings
@route.route("/user/notifications", methods=["PUT"])
@user_required
def update_notification_settings():
    identity = get_jwt_identity()
    user_data = eval(identity)
    user_id = user_data["id"]
    
    data = request.json
    notifications = data.get("notifications", [])
    
    # Here you would update the user's notification settings in a real implementation
    # For simplicity, we'll just return success
    
    return jsonify({"message": "Notification preferences saved"}), 200

# Change password
@route.route("/user/change-password", methods=["PUT"])
@user_required
def change_password():
    identity = get_jwt_identity()
    user_data = eval(identity)
    user = User.query.get(user_data["id"])
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    data = request.json
    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")
    
    # In a real implementation, you would verify the current password
    # and hash the new password before saving
    from werkzeug.security import check_password_hash, generate_password_hash
    
    if not check_password_hash(user.password, current_password):
        return jsonify({"error": "Current password is incorrect"}), 400
        
    user.password = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({"message": "Password changed successfully"}), 200

# # Fallback route for SPA
# @route.route('/<path:path>')
# def catch_all(path):
#     return send_from_directory('frontend/public', 'index.html')



# API to fetch quiz details for a user attempting it
@route.route('/user/quizzes/<int:quiz_id>', methods=['GET'])
@user_required
def get_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    quiz_data = {
        'id': quiz.id,
        'title': quiz.title,
        'time_duration': quiz.time_duration,
        'questions': [
            {
                'id': q.id,
                'question_statement': q.question_statement,
                'options': q.options  # Convert JSON string to list
            } for q in quiz.questions
        ]
    }
    
    return jsonify(quiz_data), 200

@route.route('/user/quizzes/<int:quiz_id>/submit', methods=['POST'])
@user_required
def submit_quiz(quiz_id):
    data = request.get_json()
    identity = get_jwt_identity()
    user_data = eval(identity)
    user_answers = data.get('answers', [])
    user_id = user_data['id']
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    total_questions = len(quiz.questions)
    
    if total_questions == 0:
        return jsonify({'error': 'Quiz has no questions'}), 400

    correct_answers = 0
    for idx, question in enumerate(quiz.questions):
        if idx < len(user_answers) and user_answers[idx] == question.correct_option:
            correct_answers += 1

    percentage_score = (correct_answers / total_questions) * 100

    score_entry = Score(
        quiz_id=quiz.id,
        user_id=user_id,
        total_scored=round(percentage_score, 2)  # Store as a percentage
    )
    db.session.add(score_entry)
    db.session.commit()

    return jsonify({
        'message': 'Quiz submitted successfully', 
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score_percentage': round(percentage_score, 2)
    }), 200









@route.route('/admin/get-users', methods=['GET'])
@admin_required
def get_users():
    # Fetch users with basic information
    users = User.query.filter_by(role='user').all()
    
    users_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'first_name': user.full_name.split()[0] if user.full_name else '',
        'role': user.role,
        'qualification': user.qualification,
        'dob': user.dob.isoformat() if user.dob else None,
        # 'is_active': user.is_active,  
    } for user in users]
    
    return jsonify(users_list)




@route.route('/admin/user/<int:user_id>/details', methods=['GET'])
@admin_required
def get_user_details(user_id):    
    # Fetch detailed user information with related data
    user = User.query.options(
        joinedload(User.quizzes_attempted)
    ).get_or_404(user_id)
    
    # Prepare detailed user information
    user_details = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role,
        'qualification': user.qualification,
        'dob': user.dob.isoformat() if user.dob else None,
        'quiz_attempts': [{
            'quiz_id': score.quiz_id,
            'quiz_title': score.quiz.title,
            'total_scored': score.total_scored,
            'attempt_time': score.time_stamp_of_attempt.isoformat()
        } for score in user.quizzes_attempted]
    }
    
    return jsonify(user_details)


@route.route('/admin/user/<int:user_id>/flag', methods=['PUT'])
@admin_required
def flag_user(user_id):
    # Get the user
    user = User.query.get_or_404(user_id)
    
    # Get flag status from request
    data = request.get_json()
    is_flagged = data.get('is_flagged', False)
    
    # In this example, we'll use a custom column. You might need to add this to your User model
    user.is_active = not is_flagged
    
    try:
        db.session.commit()
        return jsonify({
            "message": "User status updated successfully",
            "is_flagged": is_flagged
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update user status"}), 500

@route.route('/admin/user/<int:user_id>/scores/export', methods=['GET'])
@admin_required
def export_user_scores(user_id):
    # Fetch user's scores with related quiz information
    scores = Score.query.filter_by(user_id=user_id).join(Quiz).all()
    
    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write headers
    writer.writerow([
        'Quiz Title', 
        'Total Scored', 
        'Attempt Time', 
        'Chapter', 
        'Subject'
    ])
    
    # Write score data
    for score in scores:
        writer.writerow([
            score.quiz.title,
            score.total_scored,
            score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S'),
            score.quiz.chapter.name if score.quiz.chapter else 'N/A',
            score.quiz.chapter.subject.name if score.quiz.chapter and score.quiz.chapter.subject else 'N/A'
        ])
    
    # Convert string data to bytes
    output_bytes = io.BytesIO(output.getvalue().encode('utf-8'))
    output_bytes.seek(0)
    
    return send_file(
        output_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'user_{user_id}_scores_{datetime.now().strftime("%Y%m%d")}.csv'
    )



class AnalyticsGraphGenerator:
    # Elegant color palette
    COLOR_PALETTE = OCEAN = [
        '#4682B4',   # Steel blue
        '#48D1CC',   # Medium turquoise
        '#5F9EA0',   # Cadet blue
        '#008B8B',   # Dark cyan
        '#1E90FF',   # Dodger blue
        '#4169E1',   # Royal blue
        '#00BFFF'    # Deep sky blue
    ]

    @staticmethod
    def generate_subject_participation_graph():
        """
        Generate a graph showing quiz participation by subject with elegant styling
        """
        # Query subject participation data
        subject_participation = db.session.query(
            Subject.name, 
            func.count(Score.id).label('quiz_count')
        ).join(Chapter, Subject.id == Chapter.subject_id) \
        .join(Quiz, Quiz.chapter_id == Chapter.id) \
        .join(Score, Score.quiz_id == Quiz.id) \
        .group_by(Subject.name) \
        .order_by(func.count(Score.id).desc()) \
        .all()

        # Convert to DataFrame
        df = pd.DataFrame(subject_participation, columns=['Subject', 'Quiz Count'])

        # Set up the plot with a clean, professional style
        plt.figure(figsize=(12, 7))
        plt.style.use('seaborn-v0_8-whitegrid')  # Clean, professional grid style

        # Create the bar plot with custom color palette
        ax = sns.barplot(
            x='Subject', 
            y='Quiz Count', 
            data=df, 
            palette=AnalyticsGraphGenerator.COLOR_PALETTE
        )

        # Customize the plot
        plt.title('Quiz Participation by Subject', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Subject', fontsize=12, labelpad=10)
        plt.ylabel('Number of Quizzes', fontsize=12, labelpad=10)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)

        # Add value labels on top of each bar
        for i, v in enumerate(df['Quiz Count']):
            ax.text(
                i, 
                v, 
                str(v), 
                ha='center', 
                va='bottom', 
                fontweight='bold',
                fontsize=9
            )

        # Adjust layout and add subtle background
        plt.tight_layout()
        ax.set_facecolor('#f8f9fa')  # Light background
        plt.gcf().set_facecolor('#f8f9fa')

        # Save plot to a base64 encoded string
        return AnalyticsGraphGenerator._plot_to_base64()

    @staticmethod
    def generate_user_growth_graph():
        """
        Generate a graph showing monthly user registration with elegant styling
        """
        # Query monthly user registrations
        monthly_registrations = db.session.query(
            extract('month', User.created_at).label('month'),
            func.count(User.id).label('user_count')
        ).group_by('month') \
         .order_by('month') \
         .all()

        # Convert to DataFrame
        df = pd.DataFrame(monthly_registrations, columns=['Month', 'User Count'])
        
        # Set up the plot with a clean, professional style
        plt.figure(figsize=(12, 7))
        plt.style.use('seaborn-v0_8-whitegrid')

        # Create the line plot with custom styling
        ax = sns.lineplot(
            x='Month', 
            y='User Count', 
            data=df, 
            marker='o',
            color=AnalyticsGraphGenerator.COLOR_PALETTE[1],  # Muted green
            linewidth=2,
            markersize=10
        )

        # Customize the plot
        plt.title('Monthly User Registrations', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Month', fontsize=12, labelpad=10)
        plt.ylabel('Number of New Users', fontsize=12, labelpad=10)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)

        # Add value labels for each point
        for x, y in zip(df['Month'], df['User Count']):
            plt.text(
                x, 
                y, 
                f'{y}', 
                ha='center', 
                va='bottom', 
                fontweight='bold',
                fontsize=9
            )

        # Adjust layout and add subtle background
        plt.tight_layout()
        ax.set_facecolor('#f8f9fa')
        plt.gcf().set_facecolor('#f8f9fa')

        # Save plot to a base64 encoded string
        return AnalyticsGraphGenerator._plot_to_base64()

    @staticmethod
    def generate_performance_graph():
        """
        Generate a graph showing performance by subject with elegant styling
        """
        # Query average scores by subject
        subject_performance = db.session.query(
            Subject.name,
            func.avg(Score.total_scored).label('average_score')
        ).join(Chapter, Subject.id == Chapter.subject_id) \
        .join(Quiz, Quiz.chapter_id == Chapter.id) \
        .join(Score, Score.quiz_id == Quiz.id) \
        .group_by(Subject.name) \
        .order_by(func.avg(Score.total_scored).desc()) \
        .all()

        # Convert to DataFrame
        df = pd.DataFrame(subject_performance, columns=['Subject', 'Average Score'])

        # Set up the plot with a clean, professional style
        plt.figure(figsize=(12, 7))
        plt.style.use('seaborn-v0_8-whitegrid')

        # Create the bar plot with custom color palette
        ax = sns.barplot(
            x='Subject', 
            y='Average Score', 
            data=df, 
            palette=AnalyticsGraphGenerator.COLOR_PALETTE
        )

        # Customize the plot
        plt.title('Average Performance by Subject', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Subject', fontsize=12, labelpad=10)
        plt.ylabel('Average Score', fontsize=12, labelpad=10)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)

        # Add value labels on top of each bar
        for i, v in enumerate(df['Average Score']):
            ax.text(
                i, 
                v, 
                f'{v:.2f}', 
                ha='center', 
                va='bottom', 
                fontweight='bold',
                fontsize=9
            )

        # Adjust layout and add subtle background
        plt.tight_layout()
        ax.set_facecolor('#f8f9fa')
        plt.gcf().set_facecolor('#f8f9fa')

        # Save plot to a base64 encoded string
        return AnalyticsGraphGenerator._plot_to_base64()

    @staticmethod
    def _plot_to_base64():
        """
        Convert matplotlib plot to base64 encoded image
        """
        # Save plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        
        # Encode the bytes as base64
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        
        return image_base64

# Analytics Routes
@route.route('/admin/subject-participation-graph')
@admin_required
@cache.cached(timeout=600, key_prefix=lambda: f"subject_participation_{ast.literal_eval(get_jwt_identity())['id']}")
def subject_participation_graph():
    graph = AnalyticsGraphGenerator.generate_subject_participation_graph()
    print('hello')
    return jsonify({'graph': graph})

@route.route('/admin/user-growth-graph')
@admin_required
@cache.cached(timeout=600, key_prefix=lambda: f"user_growth_graph_{ast.literal_eval(get_jwt_identity())['id']}")
def user_growth_graph():
    graph = AnalyticsGraphGenerator.generate_user_growth_graph()
    return jsonify({'graph': graph})

@route.route('/admin/performance-graph')
@admin_required
@cache.cached(timeout=600, key_prefix=lambda: f"performance_graph_{ast.literal_eval(get_jwt_identity())['id']}")
def performance_graph():
    graph = AnalyticsGraphGenerator.generate_performance_graph()
    return jsonify({'graph': graph})

class AnalyticsGraphGeneratorUser:
    # Elegant color palette
    COLOR_PALETTE = [
        '#4682B4',  # Steel blue
        '#48D1CC',  # Medium turquoise
        '#5F9EA0',  # Cadet blue
        '#008B8B',  # Dark cyan
        '#1E90FF',  # Dodger blue
        '#4169E1',  # Royal blue
        '#00BFFF'   # Deep sky blue
    ]

    @staticmethod
    def generate_quiz_attempts_per_subject(user_id):
        """
        Generate a bar chart showing the number of quiz attempts per subject for a specific user.
        
        :param user_id: ID of the user
        :return: Base64 encoded graph image
        """
        quiz_attempts = db.session.query(
            Subject.name,
            func.count(Score.id).label('quiz_attempts')
        ).join(Chapter, Subject.id == Chapter.subject_id) \
        .join(Quiz, Quiz.chapter_id == Chapter.id) \
        .join(Score, Score.quiz_id == Quiz.id) \
        .filter(Score.user_id == user_id) \
        .group_by(Subject.name) \
        .order_by(func.count(Score.id).desc()) \
        .all()

        # Handle case when no attempts exist
        if not quiz_attempts:
            plt.figure(figsize=(12, 7))
            plt.text(0.5, 0.5, 'No Quiz Attempts Yet', 
                     horizontalalignment='center', 
                     verticalalignment='center', 
                     fontsize=16)
            plt.axis('off')
            return AnalyticsGraphGeneratorUser._plot_to_base64()

        df = pd.DataFrame(quiz_attempts, columns=['Subject', 'Quiz Attempts'])

        plt.figure(figsize=(12, 7))
        plt.style.use('seaborn-v0_8-whitegrid')

        ax = sns.barplot(
            x='Subject',
            y='Quiz Attempts',
            data=df,
            palette=AnalyticsGraphGeneratorUser.COLOR_PALETTE
        )

        plt.title('Your Quiz Attempts per Subject', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Subject', fontsize=12, labelpad=10)
        plt.ylabel('Number of Attempts', fontsize=12, labelpad=10)
        plt.xticks(rotation=45, ha='right', fontsize=10)

        # Add labels on top of bars
        for i, v in enumerate(df['Quiz Attempts']):
            ax.text(i, v, str(v), ha='center', va='bottom', fontweight='bold', fontsize=9)

        plt.tight_layout()
        return AnalyticsGraphGeneratorUser._plot_to_base64()

    @staticmethod
    def generate_average_score_per_subject(user_id):
        """
        Generate a bar chart showing the average score per subject for a specific user.
        
        :param user_id: ID of the user
        :return: Base64 encoded graph image
        """
        subject_scores = db.session.query(
            Subject.name,
            func.avg(Score.total_scored).label('average_score')
        ).join(Chapter, Subject.id == Chapter.subject_id) \
        .join(Quiz, Quiz.chapter_id == Chapter.id) \
        .join(Score, Score.quiz_id == Quiz.id) \
        .filter(Score.user_id == user_id) \
        .group_by(Subject.name) \
        .order_by(func.avg(Score.total_scored).desc()) \
        .all()

        # Handle case when no scores exist
        if not subject_scores:
            plt.figure(figsize=(12, 7))
            plt.text(0.5, 0.5, 'No Scores Available', 
                     horizontalalignment='center', 
                     verticalalignment='center', 
                     fontsize=16)
            plt.axis('off')
            return AnalyticsGraphGeneratorUser._plot_to_base64()

        df = pd.DataFrame(subject_scores, columns=['Subject', 'Average Score'])

        plt.figure(figsize=(12, 7))
        plt.style.use('seaborn-v0_8-whitegrid')

        ax = sns.barplot(
            x='Subject',
            y='Average Score',
            data=df,
            palette=AnalyticsGraphGeneratorUser.COLOR_PALETTE
        )

        plt.title('Your Average Score per Subject', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Subject', fontsize=12, labelpad=10)
        plt.ylabel('Average Score', fontsize=12, labelpad=10)
        plt.xticks(rotation=45, ha='right', fontsize=10)

        # Add labels on top of bars
        for i, v in enumerate(df['Average Score']):
            ax.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

        plt.tight_layout()
        return AnalyticsGraphGeneratorUser._plot_to_base64()

    @staticmethod
    def generate_most_attempted_course_pie(user_id):
        """
        Generate a pie chart showing the most attempted courses for a specific user.
        
        :param user_id: ID of the user
        :return: Base64 encoded graph image
        """
        course_attempts = db.session.query(
            Subject.name,
            func.count(Score.id).label('attempts')
        ).join(Chapter, Subject.id == Chapter.subject_id) \
        .join(Quiz, Quiz.chapter_id == Chapter.id) \
        .join(Score, Score.quiz_id == Quiz.id) \
        .filter(Score.user_id == user_id) \
        .group_by(Subject.name) \
        .order_by(func.count(Score.id).desc()) \
        .all()

        # Handle case when no attempts exist
        if not course_attempts:
            plt.figure(figsize=(8, 8))
            plt.text(0.5, 0.5, 'No Courses Attempted', 
                     horizontalalignment='center', 
                     verticalalignment='center', 
                     fontsize=16)
            plt.axis('off')
            return AnalyticsGraphGeneratorUser._plot_to_base64()

        df = pd.DataFrame(course_attempts, columns=['Course', 'Attempts'])

        plt.figure(figsize=(8, 8))
        plt.style.use('seaborn-v0_8-whitegrid')

        plt.pie(
            df['Attempts'],
            labels=df['Course'],
            autopct='%1.1f%%',
            colors=AnalyticsGraphGeneratorUser.COLOR_PALETTE[:len(df)],
            startangle=140,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1}
        )

        plt.title('Your Most Attempted Courses', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        return AnalyticsGraphGeneratorUser._plot_to_base64()

    @staticmethod
    def _plot_to_base64():
        """
        Convert matplotlib plot to base64 encoded image.
        """
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        
        return base64.b64encode(buf.getvalue()).decode('utf-8')

# Updated Analytics Routes
@route.route('/user/quiz-attempts-per-subject')
@user_required
@cache.cached(timeout=600, key_prefix=lambda: f"quiz_attempts_per_subject_{ast.literal_eval(get_jwt_identity())['id']}")
def quiz_attempts_per_subject():
    identity = get_jwt_identity()
    user_data = eval(identity)
    user_id = user_data['id']
    graph = AnalyticsGraphGeneratorUser.generate_quiz_attempts_per_subject(user_id)
    return jsonify({'graph': graph})

@route.route('/user/average-score-per-subject')
@user_required
@cache.cached(timeout=600, key_prefix=lambda: f"average_score_per_subject_{ast.literal_eval(get_jwt_identity())['id']}")
def average_score_per_subject():
    identity = get_jwt_identity()
    user_data = eval(identity)
    user_id = user_data['id']
    graph = AnalyticsGraphGeneratorUser.generate_average_score_per_subject(user_id)
    return jsonify({'graph': graph})

@route.route('/user/most-attempted-course')
@user_required
@cache.cached(timeout=600, key_prefix=lambda: f"most_attempted_course_{ast.literal_eval(get_jwt_identity())['id']}")
def most_attempted_course():
    identity = get_jwt_identity()
    user_data = eval(identity)
    user_id = user_data['id']
    graph = AnalyticsGraphGeneratorUser.generate_most_attempted_course_pie(user_id)
    return jsonify({'graph': graph})