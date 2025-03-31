from extensions import celery
from celery.schedules import crontab
from tasks import send_daily_reminders, generate_monthly_reports

# Schedule configuration
celery.conf.beat_schedule = {
    # Daily reminders - runs every day at 6 PM
    'send-daily-reminders': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=18, minute=0),  # 6:00 PM every day
    },
    
    # Monthly activity reports - runs on the first day of each month at 6 AM
    'monthly-activity-reports': {
        'task': 'tasks.generate_monthly_reports',
        'schedule': crontab(day_of_month=1, hour=6, minute=0),  # 6:00 AM on the first day of each month
    },
}

if __name__ == "__main__":
    celery.worker_main()