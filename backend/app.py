from datetime import datetime, time
import json
from werkzeug.security import generate_password_hash
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import redis
import os
# Import models and routes
from models import Score, db, User, Subject, Chapter, Quiz, Question
from routes import route
# At the top of app.py, after other imports
import tasks
# Import extensions
from extensions import jwt, cache, mail, make_celery, celery


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "ShreyaKhantal:)"  # Change this in production

# Redis Cache Configuration
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# Celery Configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Change if using another provider
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'MAIL_USERNAME' 
app.config['MAIL_PASSWORD'] = 'MAIL_PASSWORD'
app.config['MAIL_DEFAULT_SENDER'] = 'MAIL_SENDER'

# ==============================
# Initialize Extensions
# ==============================

# Initialize Database and Migrations
db.init_app(app)
migrate = Migrate(app, db)

# Initialize JWT
jwt.init_app(app)

# Initialize Cache
cache.init_app(app)

# Initialize Celery
celery.conf.update(app.config)
celery = make_celery(app)

# Initialize Mail
mail.init_app(app)

# Register Blueprint
app.register_blueprint(route)

# ==============================
# Redis Connection Test Route
# ==============================

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

@app.route('/cache_test')
def cache_test():
    redis_client.set("message", "Hello from Redis!")
    return redis_client.get("message")

from flask import jsonify
from flask_mail import Message
from extensions import mail

@app.route('/test_mail')
def test_mail():
    try:
        msg = Message(
            "Test Email from Quiz Master",
            recipients=["khantalshreya@gmail.com"], 
            body="This is a test email to check if Flask Mail is working."
        )
        mail.send(msg)
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/test/daily_reminder', methods=['GET'])
def test_daily_reminder():
    """Test route to manually trigger daily reminders"""
    from tasks import send_daily_reminders
    
    # Run the task synchronously for testing
    send_daily_reminders.apply()
    
    return jsonify({"message": "Daily reminder task triggered successfully"}), 200

@app.route('/test/monthly_report', methods=['GET'])
def test_monthly_report():
    """Test route to manually trigger monthly reports"""
    from tasks import generate_monthly_reports
    
    try:
        # Run the task synchronously for testing
        result = generate_monthly_reports.apply()
        print(f"Task result: {result}")
        return jsonify({"message": "Monthly report task triggered successfully"}), 200
    except Exception as e:
        print(f"Error triggering report: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # admin_exists = User.query.filter_by(email="admin@admin.com").first()
        # if not admin_exists:
        #     admin_password = generate_password_hash('admin')
        #     admin = User(username='Admin', full_name='Admin User', password=admin_password, email='admin@admin.com', role='admin')
        #     db.session.add(admin)
        
        # # Add two regular users
        # user1_exists = User.query.filter_by(email="khantalshreya@gmail.com").first()
        # if not user1_exists:
        #     user1 = User(username='Shreya Khantal', full_name='Shreya Khantal', password=generate_password_hash('12345'), email='khantalshreya@gmail.com', role='user')
        #     db.session.add(user1)
        
        # # Add two subjects
        # subject1_exists = Subject.query.filter_by(name="Mathematics").first()
        # if not subject1_exists:
        #     subject1 = Subject(name="Mathematics", description="Study of numbers and equations")
        #     db.session.add(subject1)
        
        # subject2_exists = Subject.query.filter_by(name="Science").first()
        # if not subject2_exists:
        #     subject2 = Subject(name="Science", description="Study of nature and experiments")
        #     db.session.add(subject2)
        
        # db.session.commit()
        
        # # Add chapters to subjects
        # subject1 = Subject.query.filter_by(name="Mathematics").first()
        # subject2 = Subject.query.filter_by(name="Science").first()
        
        # chapter1_exists = Chapter.query.filter_by(name="Algebra").first()
        # if not chapter1_exists:
        #     chapter1 = Chapter(name="Algebra", description="Introduction to Algebra", subject_id=subject1.id)
        #     db.session.add(chapter1)
        
        # chapter2_exists = Chapter.query.filter_by(name="Geometry").first()
        # if not chapter2_exists:
        #     chapter2 = Chapter(name="Geometry", description="Study of shapes and sizes", subject_id=subject1.id)
        #     db.session.add(chapter2)
        
        # chapter3_exists = Chapter.query.filter_by(name="Physics").first()
        # if not chapter3_exists:
        #     chapter3 = Chapter(name="Physics", description="Laws of motion and forces", subject_id=subject2.id)
        #     db.session.add(chapter3)
        
        # chapter4_exists = Chapter.query.filter_by(name="Chemistry").first()
        # if not chapter4_exists:
        #     chapter4 = Chapter(name="Chemistry", description="Chemical reactions and elements", subject_id=subject2.id)
        #     db.session.add(chapter4)
        
        # db.session.commit()
    app.run(debug=True)

# Example usage:
# from app import app, db
# with app.app_context():
#     stats = create_dummy_data(db)
#     print(stats)
