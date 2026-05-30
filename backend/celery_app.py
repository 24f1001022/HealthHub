import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

_redis = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

celery = Celery(
    'tasks',
    broker=_redis,
    backend=_redis,
)
celery.conf.imports = ('tasks',)
celery.conf.timezone = 'Asia/Kolkata'
celery.conf.beat_schedule = {
    'daily-appointment-reminder': {
        'task': 'tasks.daily_appointment_reminder',
        'schedule': crontab(hour=21, minute=42), 
    },
}
celery.conf.beat_schedule.update({
    'monthly-doctor-activity-report': {
        'task': 'tasks.send_monthly_doctor_report',
        'schedule': crontab(minute=0, hour=6, day_of_month=1),  
    },
})