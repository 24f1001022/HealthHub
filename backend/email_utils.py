from flask_mail import Message
from flask import current_app
from app import mail

def send_welcome_email(recipient):
    from app import app
    with app.app_context():
        msg = Message(
            subject='Welcome!',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[recipient],
            body=(
                "Thank you for registering with HealthHub! We’re excited to have you on board.\n"
                "Our app is designed to make managing hospital operations easier and more efficient. "
                "Whether you’re a patient or doctor, you’ll find everything you need right at your fingertips.\n"
                "If you have any questions or need assistance, feel free to reach out to our support team at 999999999.\n"
                "Welcome aboard, and we look forward to helping you!\n"
                "Best regards,\n"
                "The HealthHub Team"
            )
        )
        mail.send(msg)

def send_exportcsv_email(recipient, filepath):
    """
    Sends a professional notification email with a link to download
    the exported patient treatment CSV file.
    """
    from app import app
    with app.app_context():
        msg = Message(
            subject="Your Treatment Report is Ready",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[recipient],
            body=(
                "Dear Patient,\n\n"
                "We’ve successfully generated your treatment history report. "
                "You can securely download your CSV file using the link below:\n\n"
                f"{filepath}\n\n"
                "If you didn’t request this export, please ignore this message.\n\n"
                "Thank you for using our healthcare platform.\n\n"
                "Best regards,\n"
                "The HealthHub Team"
            )
        )
        mail.send(msg)


def send_daily_appointment_reminder_emails(appointments):
    """
    Sends reminder emails to patients with today's appointments.
    Can be imported and called from anywhere.
    """
    from app import app
    with app.app_context():
        for appt in appointments:
            patient = appt.patient
            doctor = appt.doctor
            slot = appt.slot
            message_text = (
                f"Hi {patient.full_name}, 👋\n\n"
                f"This is a reminder that you have an appointment today "
                f"with Dr. {doctor.name} at {slot}.\n\n"
                f"Please visit the hospital on time.\n\n"
                f"Have a great day!"
            )
            msg = Message(subject="Hospital Visit Reminder",recipients=[patient.email],sender=current_app.config['MAIL_USERNAME'],body=message_text)
            mail.send(msg)




def build_send_monthly_doctor_report(doctor, appointments, treatments, report_month_start):
    """
    Builds and sends the monthly doctor activity report email.
    Works similarly to send_daily_appointment_reminder_emails().
    """
    from app import app
    with app.app_context():

        html = f"""
        <html>
        <body>
            <h2>Monthly Activity Report - {report_month_start.strftime('%B %Y')}</h2>
            <h3>Doctor: {doctor.name}</h3>

            <h4>Total Appointments: {len(appointments)}</h4>
            <table border="1" cellspacing="0" cellpadding="6">
                <tr>
                    <th>Date</th>
                    <th>Patient</th>
                    <th>Time Slot</th>
                </tr>
        """

        for appt in appointments:
            html += f"""
                <tr>
                    <td>{appt.date}</td>
                    <td>{appt.patient.full_name}</td>
                    <td>{appt.slot}</td>
                </tr>
            """

        html += "</table><br><br>"

        html += """
            <h4>Treatments & Diagnosis Provided</h4>
            <table border="1" cellspacing="0" cellpadding="6">
                <tr>
                    <th>Patient</th>
                    <th>Diagnosis</th>
                    <th>Treatment</th>
                    <th>Date</th>
                </tr>
        """

        for t in treatments:
            html += f"""
                <tr>
                    <td>{t.appointment.patient.full_name}</td>
                    <td>{t.diagnosis}</td>
                    <td>{t.prescription}</td>
                    <td>{t.created_at.strftime("%Y-%m-%d")}</td>
                </tr>
            """

        html += "</table></body></html>"
        msg = Message(
            subject=f"Monthly Report - {report_month_start.strftime('%B %Y')}",
            recipients=[doctor.email],
            sender=app.config['MAIL_USERNAME'],
            html=html
        )


        mail.send(msg)