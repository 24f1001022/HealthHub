from flask import Blueprint, jsonify, session,current_app, request
import time
from models.models import User,Department,Appointment,db,DoctorSlot,Doctor,PatientTreatment
from app import cache
from datetime import date,datetime,timedelta

patient_bp = Blueprint('patient', __name__)


def _format_medicines(medicines):
    if not medicines:
        return ''
    if isinstance(medicines, list):
        parts = []
        for m in medicines:
            if isinstance(m, dict):
                parts.append(m.get('name', str(m)))
            else:
                parts.append(str(m))
        return ', '.join(parts)
    return str(medicines)


@patient_bp.route('/api/patient/<int:id>')
def patient(id):
    patient_trt_data = PatientTreatment.query.filter_by(patient_id=id).first()

    if not patient_trt_data:
        return jsonify({'message': 'No appointment or treatment details found for this patient'}), 404

    data = {
        'name': patient_trt_data.appointment.patient.full_name,
        'gender': patient_trt_data.appointment.patient.gender,
        'visit_type': patient_trt_data.visit_type or "",
        'diagnosis': patient_trt_data.diagnosis or "",
        'prescription': patient_trt_data.prescription or "",
        'test_done': patient_trt_data.test_done or "",
        'medicines': patient_trt_data.medicines or "",
        'appointment_id':patient_trt_data.appointment.id,
    }

    return jsonify(data), 200

@patient_bp.route("/api/patient/<int:patient_id>/profile", methods=["GET"])
def get_patient_profile(patient_id):
    patient = User.query.get(patient_id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    return jsonify({
        "id": patient.id,
        "name": patient.full_name,
        "age": patient.age,
        "gender": patient.gender,
        "email": patient.email,
        "phone": patient.phone_no,
        "address": patient.address,
    })

@patient_bp.route("/api/patient/<int:patient_id>/profile", methods=["PUT"])
def update_patient_profile(patient_id):
    patient = User.query.get(patient_id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    data = request.get_json()
    patient.full_name = data.get("name", patient.full_name)
    patient.age = data.get("age", patient.age)
    patient.gender = data.get("gender", patient.gender)
    patient.email = data.get("email", patient.email)
    patient.phone_no = data.get("phone", patient.phone_no)
    patient.address = data.get("address", patient.address)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})



@patient_bp.route('/api/doctor/<int:id>')
def doctor_details(id):
    if session.get('role')!= 'patient':
        return jsonify({'message': 'Access denied'}), 403
    doctor = Doctor.query.filter_by(id=id).first()
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    data ={
        'id' :doctor.id,
        'name':doctor.name,
        'experience':doctor.experience,
        'department_name':doctor.department_name,
        'email' : doctor.email,
        'gender' : doctor.gender
    }
    return jsonify(data)
@patient_bp.route('/api/patient/dashboard')
def patient_dashboard():
    if session.get('role') != 'patient':
        return jsonify({'message': 'Access denied'}), 403

    user_id = session.get('user_id')
    cache_key = f"patient_dashboard:{user_id}"

    cached_data = cache.get(cache_key)
    if cached_data:
        return jsonify(cached_data)

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    APPOINTMENTS=Appointment.query.filter_by(patient_id=user_id,status='booked').all()
    appointment=[{'id': a.id, 'doctor': a.doctor.name, 'department': a.doctor.department_name, 'date': a.date.strftime("%Y-%m-%d") , 'time': a.slot} for a in APPOINTMENTS]
    depts = Department.query.all()
    data = {
        'user_name': user.full_name.capitalize(),
        'departments': [{"id": d.id, "name": d.dpt_name} for d in depts],
        'appointments': appointment,
        'user_id' : user_id
    }

    cache.set(cache_key, data, timeout=50)
    return jsonify(data)

@patient_bp.route('/api/patient/cancel/<int:appt_id>', methods=['POST'])
def cancel_appointment(appt_id):
    if session.get('role') != 'patient':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    appointment = Appointment.query.filter_by(id=appt_id, patient_id=session.get('user_id')).first()
    if not appointment:
        return jsonify({'success': False, 'message': 'Appointment not found'}), 404
    slot = DoctorSlot.query.filter_by(appointment_id=appt_id).first()
    print(slot)
    if slot:
        slot.status = 'available'
        slot.appointment_id = None 
    appointment.status = 'cancelled'
    db.session.commit()
    user_id = session.get('user_id')
    if user_id:
        cache.delete(f"patient_dashboard:{user_id}")

    return jsonify({'success': True, 'message': f'Appointment {appt_id} cancelled successfully'})

@patient_bp.route('/api/patient/department/<int:dept_id>')
def department_details(dept_id):
    if session.get('role') != 'patient':
        return jsonify({'message': 'Access denied'}), 403

    cache_key = f"department:{dept_id}"
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)

    dept = Department.query.filter_by(id=dept_id).first()

    if not dept:
        return jsonify({'message': 'Department not found'}), 404
    response = {
        "id": dept.id,
        "name": dept.dpt_name,
        "overview": dept.description,
        "doctors": [
            {"id": d.id, "name": d.name}
            for d in dept.doctors_registered
        ]
    }

    cache.set(cache_key, response, timeout=10)
    return jsonify(response)



@patient_bp.route('/api/doctor/<int:doctor_id>/availability', methods=['GET'])
def get_doctor_slots(doctor_id):
    today = date.today()
    end_date = today + timedelta(days=7)

    slots = DoctorSlot.query.filter(
        DoctorSlot.doctor_id == doctor_id,
        DoctorSlot.date >= today,
        DoctorSlot.date <= end_date
    ).order_by(DoctorSlot.date, DoctorSlot.start_time).all()

    grouped = {}
    for s in slots:
        d = s.date.strftime('%d/%m/%Y')
        grouped.setdefault(d, []).append(s.serialize())

    return jsonify(grouped)


@patient_bp.route('/api/book-slot', methods=['POST'])
def book_slot():
    data = request.get_json()
    slot_id = data.get('slot_id')
    patient_id = session.get('user_id')

    if not patient_id:
        return jsonify({'message': 'Please login as patient'}), 401

    slot = DoctorSlot.query.get(slot_id)
    if not slot:
        return jsonify({'message': 'Slot not found'}), 404

    if str(slot.status).lower() == 'booked':
        return jsonify({'message': 'This slot is already booked'}), 400
    if str(slot.status).lower() != 'available':
        return jsonify({'message': 'This slot is not available for booking'}), 400
    appointment = Appointment(
        doctor_id=slot.doctor_id,
        patient_id=patient_id,
        date=slot.date,
        slot=f"{slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}",
        status='booked'
    )
    patient_trt=PatientTreatment(
        appointment=appointment,
        patient_id=patient_id,
        doctor_id=slot.doctor_id
    )
    db.session.add(appointment)
    db.session.add(patient_trt)
    db.session.flush()
    slot.status = 'booked'
    slot.appointment_id = appointment.id
    db.session.commit()
    user_id = session.get('user_id')
    if user_id:
        cache.delete(f"patient_dashboard:{user_id}")

    return jsonify({'success': True, 'message': 'Appointment booked successfully'})

@patient_bp.route('/api/patient/<int:patient_id>/treatment', methods=['POST'])
def update_treatment(patient_id):
    if session.get('role') != 'doctor':
        return jsonify({'message': 'Access denied'}), 403

    data = request.get_json()
    new_treatment = PatientTreatment(
        patient_id=patient_id,
        appointment_id=data.get("appointment_id"),
        doctor_id=session.get('user_id'),
        visit_type=data.get('visit_type'),
        test_done=data.get('test_done'),
        diagnosis=data.get('diagnosis'),
        prescription=data.get('prescription'),
        medicines=data.get('medicines', [])
    )
    db.session.add(new_treatment)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Treatment updated successfully!'})


@patient_bp.route('/api/patient/<int:patient_id>/treatment', methods=['GET'])
def get_treatment(patient_id):
    treatments = PatientTreatment.query.filter_by(patient_id=patient_id).order_by(PatientTreatment.created_at.desc()).all()
    return jsonify([t.serialize() for t in treatments])


@patient_bp.route("/api/patient/<int:patient_id>/history", methods=["GET"])
def get_patient_history(patient_id):
    treatments = (
        PatientTreatment.query.filter_by(patient_id=patient_id)
        .order_by(PatientTreatment.created_at.asc())
        .all()
    )

    if not treatments:
        return jsonify({"message": "No history found", "history": []}), 200

    patient = User.query.filter_by(id=patient_id).first()
    doctor = Doctor.query.filter_by(id=treatments[0].doctor_id).first()

    patient_name = patient.full_name if patient else "Unknown"
    doctor_name = doctor.name if doctor else "Unknown"
    department_name = doctor.department.dpt_name if doctor and doctor.department else "Unknown"

    history_data = {
        "patient_name": patient_name,
        "doctor_name": doctor_name,
        "department": department_name,
        "records": [
            {
                "visit_no": idx + 1,
                "visit_type": t.visit_type,
                "tests_done": t.test_done,
                "diagnosis": t.diagnosis,
                "prescription": t.prescription,
                "medicines": _format_medicines(t.medicines),
            }
            for idx, t in enumerate(treatments)
        ],
    }

    return jsonify(history_data), 200
