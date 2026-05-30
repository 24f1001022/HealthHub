from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db=SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    age = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.String(10))
    phone_no = db.Column(db.String(10),nullable=False)
    passhash = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(120))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), nullable=False, default="patient")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

class Doctor(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    department_name = db.Column(db.String(25),nullable=False)
    experience = db.Column(db.String(10))
    email = db.Column(db.String(120), unique=True, nullable=False) 
    gender = db.Column(db.String(10))
    phone_no = db.Column(db.String(10),nullable=False)
    passhash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="doctor") 
    dpt_id = db.Column(db.Integer,db.ForeignKey('department.id'),nullable=False) 

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

class DoctorSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='unavailable')  # available / booked / unavailable
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%d/%m/%Y'),
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M'),
            'status': self.status
        }


class Appointment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    patient_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    doctor_id = db.Column(db.Integer,db.ForeignKey("doctor.id"),nullable=False)
    date = db.Column(db.Date, nullable=False)
    slot = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='booked')  # booked / completed / canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    doctor = db.relationship('Doctor', backref='appointments')
    patient = db.relationship('User', backref='appointments') 

class PatientTreatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id')) 
    visit_type = db.Column(db.String(100))
    test_done = db.Column(db.String(255))
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    medicines = db.Column(db.JSON)  # example: [{"name": "Paracetamol", "dosage": "1-0-1"}]
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    appointment = db.relationship('Appointment', backref='treatment')

    def serialize(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "appointment_id": self.appointment_id,
            "appointment_date": self.appointment.date.strftime("%Y-%m-%d") if self.appointment else None,
            "appointment_slot": self.appointment.slot if self.appointment else None,
            "visit_type": self.visit_type,
            "test_done": self.test_done,
            "diagnosis": self.diagnosis,
            "prescription": self.prescription,
            "medicines": self.medicines,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

class Department(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    dpt_name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    doctors_registered = db.relationship('Doctor', backref='department', lazy=True)
