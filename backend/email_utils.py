import logging
from flask import current_app
from flask_mail import Message
from app import mail

logger = logging.getLogger(__name__)


def _mail_configured():
    username = current_app.config.get('MAIL_USERNAME')
    password = current_app.config.get('MAIL_PASSWORD')
    return bool(username and password)


def _sender():
    default = current_app.config.get('MAIL_DEFAULT_SENDER')
    if default:
        return default
    username = current_app.config.get('MAIL_USERNAME')
    return ('HealthHub', username) if username else None


def send_welcome_email(recipient):
    if not _mail_configured():
        logger.warning('Welcome email skipped: MAIL_USERNAME or MAIL_PASSWORD not set')
        return False

    frontend = current_app.config.get('FRONTEND_URL', 'http://localhost:5173')
    msg = Message(
        subject='Welcome to HealthHub!',
        sender=_sender(),
        recipients=[recipient],
        body=(
            f'Thank you for registering with HealthHub!\n\n'
            f'Your account is ready. Sign in anytime at:\n{frontend}/login\n\n'
            f'If you did not create this account, you can ignore this email.\n\n'
            f'Best regards,\nThe HealthHub Team'
        ),
        html=f'''
        <div style="font-family:Segoe UI,sans-serif;max-width:560px;margin:0 auto;padding:24px;">
          <h2 style="color:#0d6efd;">Welcome to HealthHub</h2>
          <p>Thank you for registering. Your patient account is active.</p>
          <p><a href="{frontend}/login" style="background:#0d6efd;color:#fff;padding:12px 24px;text-decoration:none;border-radius:8px;display:inline-block;">Sign in to HealthHub</a></p>
          <p style="color:#666;font-size:14px;">If you did not create this account, ignore this email.</p>
          <p>— The HealthHub Team</p>
        </div>
        ''',
    )
    mail.send(msg)
    logger.info('Welcome email sent to %s', recipient)
    return True


def send_exportcsv_email(recipient, filepath):
    if not _mail_configured():
        return False
    msg = Message(
        subject='Your Treatment Report is Ready',
        sender=_sender(),
        recipients=[recipient],
        body=(
            'Dear Patient,\n\n'
            'Your treatment history report is ready:\n\n'
            f'{filepath}\n\n'
            'If you did not request this export, ignore this message.\n\n'
            '— The HealthHub Team'
        ),
    )
    mail.send(msg)
    return True


def send_daily_appointment_reminder_emails(appointments):
    if not _mail_configured():
        return
    for appt in appointments:
        patient = appt.patient
        doctor = appt.doctor
        slot = appt.slot
        message_text = (
            f'Hi {patient.full_name},\n\n'
            f'Reminder: appointment today with Dr. {doctor.name} at {slot}.\n\n'
            f'Please arrive on time.\n\n— HealthHub'
        )
        msg = Message(
            subject='Hospital Visit Reminder',
            recipients=[patient.email],
            sender=_sender(),
            body=message_text,
        )
        mail.send(msg)


def build_send_monthly_doctor_report(doctor, appointments, treatments, report_month_start):
    if not _mail_configured():
        return
    html = f'''
    <html><body>
        <h2>Monthly Activity Report - {report_month_start.strftime('%B %Y')}</h2>
        <h3>Doctor: {doctor.name}</h3>
        <h4>Total Appointments: {len(appointments)}</h4>
        <table border="1" cellspacing="0" cellpadding="6">
            <tr><th>Date</th><th>Patient</th><th>Time Slot</th></tr>
    '''
    for appt in appointments:
        html += f'<tr><td>{appt.date}</td><td>{appt.patient.full_name}</td><td>{appt.slot}</td></tr>'
    html += '</table><br><h4>Treatments</h4><table border="1" cellspacing="0" cellpadding="6">'
    html += '<tr><th>Patient</th><th>Diagnosis</th><th>Treatment</th><th>Date</th></tr>'
    for t in treatments:
        html += f'''
            <tr>
                <td>{t.appointment.patient.full_name if t.appointment else ""}</td>
                <td>{t.diagnosis or ""}</td>
                <td>{t.prescription or ""}</td>
                <td>{t.created_at.strftime("%Y-%m-%d")}</td>
            </tr>
        '''
    html += '</table></body></html>'
    msg = Message(
        subject=f'Monthly Report - {report_month_start.strftime("%B %Y")}',
        recipients=[doctor.email],
        sender=_sender(),
        html=html,
    )
    mail.send(msg)
