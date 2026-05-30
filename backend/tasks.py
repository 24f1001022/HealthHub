import os
import csv
import uuid
from datetime import datetime, date, timedelta
from models.models import db, User, PatientTreatment, Appointment, Doctor
from email_utils import (
    send_welcome_email,
    send_exportcsv_email,
    send_daily_appointment_reminder_emails,
    build_send_monthly_doctor_report,
)
import config

_redis = None


def _get_redis():
    global _redis
    if not config.USE_REDIS:
        return None
    if _redis is None:
        from redis import Redis
        _redis = Redis.from_url(config.REDIS_URL)
    return _redis


def _set_export_status(redis_key, mapping):
    r = _get_redis()
    if r:
        r.hset(redis_key, mapping=mapping)
        r.expire(redis_key, 24 * 3600)


def make_export_folder():
    folder = os.path.join(os.getcwd(), 'exports')
    os.makedirs(folder, exist_ok=True)
    return folder


def export_patient_treatments_sync(patient_id, email=None, task_id=None):
    """Run CSV export in-process (no Celery). Returns filepath."""
    task_id = task_id or str(uuid.uuid4())
    redis_key = f'export:{patient_id}:{task_id}'
    _set_export_status(redis_key, {'status': 'started'})

    from app import app

    with app.app_context():
        patient = User.query.get(patient_id)
        if not patient:
            _set_export_status(redis_key, {'status': 'failed', 'error': 'Patient not found'})
            raise ValueError('Patient not found')

        treatments = (
            PatientTreatment.query.join(Appointment, isouter=True)
            .filter(
                PatientTreatment.patient_id == patient_id,
                PatientTreatment.visit_type.isnot(None),
            )
            .all()
        )

        folder = make_export_folder()
        filename = f'patient_{patient_id}_treatments_{datetime.utcnow().strftime("%Y%m%d")}.csv'
        filepath = os.path.join(folder, filename)

        headers = [
            'user_id', 'username', 'consulting_doctor_id',
            'appointment_date', 'Visit_Type', 'diagnosis', 'treatment', 'created_at',
        ]

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for t in treatments:
                writer.writerow([
                    patient.id,
                    patient.full_name,
                    t.doctor_id,
                    t.appointment.date.strftime('%Y-%m-%d') if t.appointment else '',
                    t.visit_type,
                    t.diagnosis or '',
                    t.prescription or '',
                    t.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                ])

        _set_export_status(redis_key, {'status': 'finished', 'filepath': filepath})

        if email:
            try:
                base = config.PUBLIC_BASE_URL.rstrip('/')
                file_url = f'{base}/exports/{os.path.basename(filepath)}'
                send_exportcsv_email(email, filepath=file_url)
            except Exception as e:
                _set_export_status(redis_key, {'email_error': str(e)})

        return filepath, task_id


def run_daily_appointment_reminder():
    from app import app
    with app.app_context():
        today = date.today()
        appointments = Appointment.query.filter_by(date=today).all()
        if not appointments:
            return 'No appointments today.'
        send_daily_appointment_reminder_emails(appointments)
        return 'Daily reminders processed.'


def run_monthly_doctor_report():
    from app import app
    with app.app_context():
        today = date.today()
        first_day = today.replace(day=1)
        last_month_end = first_day - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        for doctor in Doctor.query.all():
            try:
                appointments = Appointment.query.filter(
                    Appointment.doctor_id == doctor.id,
                    Appointment.date >= last_month_start,
                    Appointment.date <= last_month_end,
                ).all()
                treatments = PatientTreatment.query.filter(
                    PatientTreatment.doctor_id == doctor.id,
                    PatientTreatment.visit_type.isnot(None),
                    PatientTreatment.created_at >= last_month_start,
                    PatientTreatment.created_at <= last_month_end,
                ).all()
                build_send_monthly_doctor_report(
                    doctor, appointments, treatments, last_month_start
                )
            except Exception as e:
                print(f'ERROR report for {doctor.email}: {e}')
        return 'Monthly reports processed.'


# Optional Celery (local dev with worker running)
if config.USE_CELERY:
    from celery_app import celery

    @celery.task
    def send_welcome_email_task(email):
        send_welcome_email(email)

    @celery.task(name='tasks.export_patient_treatments_task', bind=True)
    def export_patient_treatments_task(self, patient_id, email=None):
        export_patient_treatments_sync(patient_id, email, task_id=self.request.id)

    @celery.task(name='tasks.daily_appointment_reminder')
    def daily_appointment_reminder():
        return run_daily_appointment_reminder()

    @celery.task(name='tasks.send_monthly_doctor_report')
    def send_monthly_doctor_report():
        return run_monthly_doctor_report()
