from datetime import datetime, timedelta
from jinja2 import Template
from matplotlib import pyplot as plt
from sqlalchemy import desc, extract, func
from flask_mail import Message
from models import db, User, Quiz, Subject, Chapter, Score
from extensions import mail, celery

@celery.task
def send_daily_reminders():
    """Send daily email reminders to users who haven't logged in or have new quizzes available"""
    today = datetime.utcnow().date()
    
    # Get all users
    users = User.query.all()
    
    for user in users:
        # Skip admin users (assuming role field determines this)
        if user.role == 'admin':
            continue
            
        # Check if user hasn't logged in today
        not_logged_in_today = user.last_login.date() < today
        
        # Find quizzes created today
        new_quizzes = Quiz.query.filter(Quiz.date_of_quiz == today).all()
        
        # Only send reminder if user hasn't logged in or there are new quizzes
        if not_logged_in_today or new_quizzes:
            send_reminder_email(user, new_quizzes, not_logged_in_today)

def send_reminder_email(user, new_quizzes, not_logged_in):
    """Send a personalized reminder email to the user"""
    # Create subject line
    if new_quizzes and not_logged_in:
        email_subject = f"Quiz Master - New quizzes available!"
    elif new_quizzes:
        email_subject = f"Quiz Master - {len(new_quizzes)} new quiz(es) available today!"
    else:
        email_subject = "Quiz Master - We miss you! Log in today"

    # Create message body
    body = f"Hello {user.full_name},\n\n"
    
    if not_logged_in:
        body += "We've noticed you haven't visited Quiz Master today. "
        body += "Log in to keep your learning streak going!\n\n"
    
    if new_quizzes:
        body += f"There {'is' if len(new_quizzes) == 1 else 'are'} {len(new_quizzes)} new quiz(es) available today:\n\n"
        
        for quiz in new_quizzes:
            chapter = Chapter.query.get(quiz.chapter_id)
            subject = Subject.query.get(chapter.subject_id)
            body += f"• {quiz.title} - {chapter.name} ({subject.name})\n"
            if quiz.time_duration:
                body += f"  Duration: {quiz.time_duration}\n"
            if quiz.remarks:
                body += f"  Remarks: {quiz.remarks}\n"
            body += "\n"
    
    body += "Visit Quiz Master now to attempt these quizzes and improve your knowledge!\n\n"
    body += "Best regards,\nThe Quiz Master Team"
    
    # Send email
    try:
        # Print for debugging
        print(f"Sending email to user {user.id} with email: {user.email}, type: {type(user.email)}")
        
        # Make sure email is a string
        user_email = str(user.email) if hasattr(user, 'email') else None
        
        if not user_email:
            print(f"User {user.id} has no valid email address")
            return
            
        msg = Message(email_subject, recipients=[user_email])
        msg.body = body
        mail.send(msg)
        print(f"Successfully sent reminder email to {user_email}")
    except Exception as e:
        print(f"Error sending reminder email to user {user.id}: {str(e)}")

@celery.task
def generate_monthly_reports():
    """Generate and send monthly activity reports for all users on the first day of each month"""
    # Get previous month and year
    today = datetime.utcnow()
    if today.month == 1:  # January
        report_month = 12
        report_year = today.year - 1
    else:
        report_month = today.month - 1
        report_year = today.year
    
    # Get all regular users
    users = User.query.filter(User.role == 'user').all()
    
    for user in users:
        # Generate and send report for each user
        print('hello')
        generate_user_report(user, report_month, report_year)

def generate_user_report(user, month, year):
    """Generate and send a monthly activity report for a specific user"""
    # Get month name for display
    month_name = datetime(year, month, 1).strftime('%B')
    
    # Get all quizzes attempted by the user in the specified month
    month_name = datetime(year, month, 1).strftime('%B')
    user_scores = Score.query.filter(
        Score.user_id == user.id,
        extract('month', Score.time_stamp_of_attempt) == month,
        extract('year', Score.time_stamp_of_attempt) == year
    ).all()
    print(user_scores)
    if not user_scores:
        # Create a special "no activity" report instead
        send_no_activity_report(user, month_name, year)
        return
    
    # Collect quiz data
    quiz_data = []
    subject_performance = {}
    total_score = 0
    
    for score in user_scores:
        quiz = Quiz.query.get(score.quiz_id)
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)
        
        # Add to quiz data list
        quiz_data.append({
            'quiz_title': quiz.title,
            'subject': subject.name,
            'chapter': chapter.name,
            'date': score.time_stamp_of_attempt.strftime('%Y-%m-%d'),
            'score': score.total_scored
        })
        
        # Add to subject performance tracking
        if subject.name not in subject_performance:
            subject_performance[subject.name] = {
                'attempts': 0,
                'total_score': 0
            }
        
        subject_performance[subject.name]['attempts'] += 1
        subject_performance[subject.name]['total_score'] += score.total_scored
        total_score += score.total_scored
    
    # Calculate average score
    avg_score = total_score / len(user_scores)
    
    # Calculate average score per subject
    for subject in subject_performance:
        subject_performance[subject]['avg_score'] = (
            subject_performance[subject]['total_score'] / subject_performance[subject]['attempts']
        )
    
    # Get user ranking
    # First, get average scores for all users in this month
    user_rankings = db.session.query(
        Score.user_id,
        func.avg(Score.total_scored).label('avg_score')
    ).filter(
        extract('month', Score.time_stamp_of_attempt) == month,
        extract('year', Score.time_stamp_of_attempt) == year
    ).group_by(Score.user_id).order_by(desc('avg_score')).all()
    
    # Find user's rank
    user_rank = None
    total_users = len(user_rankings)
    
    for i, (user_id, _) in enumerate(user_rankings):
        if user_id == user.id:
            user_rank = i + 1
            break
    

    # Generate HTML report
    html_content = create_monthly_report_html(
        user=user,
        month_name=month_name,
        year=year,
        quiz_data=quiz_data,
        avg_score=avg_score,
        subject_performance=subject_performance,
        user_rank=user_rank,
        total_users=total_users
    )
    print('generate user report')
    # Send email with report
    subject = f"Quiz Master - Your {month_name} {year} Activity Report"
    send_report_email(user.email, subject, html_content)

def create_monthly_report_html(user, month_name, year, quiz_data, avg_score, 
                              subject_performance, user_rank, total_users):
    """Create HTML content for the monthly report"""
    template_str = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            h2 { color: #3498db; margin-top: 30px; }
            .stat-box { background-color: #f8f9fa; border-radius: 5px; padding: 15px; margin: 15px 0; }
            .highlight { color: #e74c3c; font-weight: bold; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #3498db; color: white; }
            tr:hover { background-color: #f5f5f5; }
            .chart { margin: 20px 0; text-align: center; }
        </style>
    </head>
    <body>
        <h1>Monthly Activity Report - {{ month_name }} {{ year }}</h1>
        
        <p>Hello {{ user.full_name }},</p>
        
        <p>Here's your activity summary for {{ month_name }} {{ year }} on Quiz Master:</p>
        
        <div class="stat-box">
            <h2>Summary</h2>
            <p>Quizzes Attempted: <span class="highlight">{{ quiz_data|length }}</span></p>
            <p>Average Score: <span class="highlight">{{ "%.2f"|format(avg_score) }}</span></p>
            {% if user_rank %}
            <p>Your Ranking: <span class="highlight">{{ user_rank }}</span> out of {{ total_users }} users</p>
            {% endif %}
        </div>
        
        <h2>Quiz Performance Details</h2>
        <table>
            <tr>
                <th>Quiz</th>
                <th>Subject</th>
                <th>Chapter</th>
                <th>Date</th>
                <th>Score</th>
            </tr>
            {% for quiz in quiz_data %}
            <tr>
                <td>{{ quiz.quiz_title }}</td>
                <td>{{ quiz.subject }}</td>
                <td>{{ quiz.chapter }}</td>
                <td>{{ quiz.date }}</td>
                <td>{{ quiz.score }}</td>
            </tr>
            {% endfor %}
        </table>
        
        <h2>Performance by Subject</h2>
        <table>
            <tr>
                <th>Subject</th>
                <th>Attempts</th>
                <th>Average Score</th>
            </tr>
            {% for subject, data in subject_performance.items() %}
            <tr>
                <td>{{ subject }}</td>
                <td>{{ data.attempts }}</td>
                <td>{{ "%.2f"|format(data.avg_score) }}</td>
            </tr>
            {% endfor %}
        </table>
        
        
        
        <div class="stat-box">
            <h2>Recommendations</h2>
            <p>Based on your performance this month:</p>
            <ul>
                {% if subject_performance|length > 0 %}
                {% set min_subject = subject_performance.items()|list|sort(attribute='1.avg_score')|first %}
                <li>Consider focusing more on <strong>{{ min_subject[0] }}</strong> where your average score is {{ "%.2f"|format(min_subject[1].avg_score) }}.</li>
                {% endif %}
                
                {% if quiz_data|length < 5 %}
                <li>Try to attempt more quizzes next month to improve your overall performance.</li>
                {% endif %}
                
                {% if user_rank and user_rank > (total_users / 2) %}
                <li>Your ranking is below average. Keep practicing to improve your standing!</li>
                {% endif %}
            </ul>
        </div>
        
        <p>Looking forward to seeing your progress next month!</p>
        <p>Best regards,<br>The Quiz Master Team</p>
    </body>
    </html>
    """
    print('monthly report creation')
    template = Template(template_str)
    return template.render(
        user=user,
        month_name=month_name,
        year=year,
        quiz_data=quiz_data,
        avg_score=avg_score,
        subject_performance=subject_performance,
        user_rank=user_rank,
        total_users=total_users,
    )

def send_report_email(email, subject, html_content):
    """Send the monthly report email"""
    try:
        
        print('send report email')
        msg = Message(subject, recipients=[email])
        msg.html = html_content
        mail.send(msg)
    except Exception as e:
        print(f"Error sending monthly report to {email}: {str(e)}")

def send_no_activity_report(user, month_name, year):
    """Send a report to users with no quiz activity"""
    try:
        subject = f"Quiz Master - Your {month_name} {year} Activity Report"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                .message-box {{ background-color: #f8f9fa; border-radius: 5px; padding: 20px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1>Monthly Activity Report - {month_name} {year}</h1>
            
            <p>Hello {user.full_name},</p>
            
            <div class="message-box">
                <p>We noticed you didn't attempt any quizzes during {month_name} {year}.</p>
                <p>Regular practice is key to improving your knowledge and skills. We encourage you to log in and take some quizzes this month!</p>
            </div>
            
            <p>Looking forward to seeing your activity next month!</p>
            <p>Best regards,<br>The Quiz Master Team</p>
        </body>
        </html>
        """
        
        msg = Message(subject, recipients=[user.email])
        msg.html = html_content
        mail.send(msg)
        print(f"No activity report sent to {user.email}")
    except Exception as e:
        print(f"Error sending no-activity report to {user.email}: {str(e)}")