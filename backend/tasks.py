import os
import csv
from datetime import datetime,date,timedelta
from redis import Redis
from flask_mail import Mail, Message
from models.models import db, User, PatientTreatment,Appointment,Doctor
from email_utils import send_welcome_email,send_exportcsv_email,send_daily_appointment_reminder_emails,build_send_monthly_doctor_report
import config
from sqlalchemy import not_, or_, and_
from celery_app import celery 

r = Redis.from_url(config.REDIS_URL)


@celery.task
def send_welcome_email_task(email):
    send_welcome_email(email)


def make_export_folder():
    folder = os.path.join(os.getcwd(), "exports")
    os.makedirs(folder, exist_ok=True)
    return folder


@celery.task(name='tasks.export_patient_treatments_task', bind=True)
def export_patient_treatments_task(self, patient_id, email=None):
    """
    Celery background task: export patient treatments as CSV,
    store in /exports folder, mark status in Redis, and email user when done.
    """
    task_id = self.request.id
    redis_key = f"export:{patient_id}:{task_id}"
    r.hset(redis_key, mapping={"status": "started"})
    r.expire(redis_key, 24 * 3600)

    try:
        from app import app,mail

        with app.app_context():
            patient = User.query.get(patient_id)
            treatments = (PatientTreatment.query.join(Appointment, isouter=True).filter(PatientTreatment.patient_id == patient_id,PatientTreatment.visit_type.isnot(None)).all())

            folder = make_export_folder()
            filename = f"patient_{patient_id}_treatments_{datetime.utcnow().strftime('%Y%m%d')}.csv"
            filepath = os.path.join(folder, filename)

            headers = [
                "user_id", "username", "consulting_doctor_id",
                "appointment_date","Visit_Type","diagnosis", "treatment", "created_at"
            ]

            with open(filepath, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)

                for t in treatments:
                    writer.writerow([
                        patient.id,
                        patient.full_name,
                        t.doctor_id,
                        t.appointment.date.strftime("%Y-%m-%d") if t.appointment else "",
                        t.visit_type,
                        t.diagnosis or "",
                        t.prescription or "",
                        t.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    ])

            r.hset(redis_key, mapping={"status": "finished", "filepath": filepath})
            r.expire(redis_key, 24 * 3600)
            print(email)

            if email:
                try:
                    file_url = f"http://localhost:5000/exports/{os.path.basename(filepath)}"
                    send_exportcsv_email(email, filepath=file_url)
                    print(f"Export email sent to {email}")
                except Exception as e:
                    print(f"Failed to send export email: {e}")
                    r.hset(redis_key, "email_error", str(e))


    except Exception as e:
        r.hset(redis_key, mapping={"status": "failed", "error": str(e)})
        raise


@celery.task(name='tasks.daily_appointment_reminder')
def daily_appointment_reminder():
    try:
        from datetime import date
        from app import app 
        with app.app_context(): 
            today = date.today()
            appointments = Appointment.query.filter_by(date=today).all()

            if not appointments:
                print("No appointments for today.")
                return "No appointments today."
            send_daily_appointment_reminder_emails(appointments)
            print("Daily reminders processed successfully.")
            return "Daily reminders processed."

    except Exception as e:
        print(f"Error in daily_appointment_reminder task: {e}")
        return f"Task failed: {str(e)}"



@celery.task(name="tasks.send_monthly_doctor_report")
def send_monthly_doctor_report():
    from app import app

    with app.app_context():

        today = date.today()
        first_day = today.replace(day=1)
        last_month_end = first_day - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        doctors = Doctor.query.filter_by().all()

        for doctor in doctors:

            try:
                appointments = Appointment.query.filter(
                    Appointment.doctor_id == doctor.id,
                    Appointment.date >= last_month_start,
                    Appointment.date <= last_month_end
                ).all()
                treatments = PatientTreatment.query.filter(
                    PatientTreatment.doctor_id == doctor.id,
                    PatientTreatment.visit_type.isnot(None),
                    PatientTreatment.created_at >= last_month_start,
                    PatientTreatment.created_at <= last_month_end
                ).all()

                build_send_monthly_doctor_report(
                    doctor,
                    appointments,
                    treatments,
                    last_month_start
                )

                print(f"Successfully processed report for {doctor.email}")

            except Exception as e:
                print(f"ERROR generating/sending report for {doctor.email}: {e}")
