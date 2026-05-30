from flask import Blueprint, jsonify, session,request
from models.models import Doctor,db,DoctorSlot,Appointment
from datetime import datetime, timedelta,date,time
from app import cache

doctor_bp = Blueprint('doctor', __name__)

#------UTILITY----------------
def create_daily_slots(doctor_id, date_obj):
    start = datetime.combine(date_obj, time(9, 0))
    end = datetime.combine(date_obj, time(16, 0))
    slots = []
    while start < end:
        slot = DoctorSlot(
            doctor_id=doctor_id,
            date=date_obj,
            start_time=start.time(),
            end_time=(start + timedelta(minutes=30)).time(),
            status='unavailable'
        )
        db.session.add(slot)
        slots.append(slot)
        start += timedelta(minutes=30)
    db.session.commit()
    return slots

#------ Ends-------------------------------

@doctor_bp.route('/api/doctor/dashboard', methods=['GET'])
def doctor_dashboard():
    if session.get('role') != 'doctor':
        return jsonify({'message': 'Access denied'}), 403

    doctor_id = session.get('user_id')
    cache_key = f"doctor_dashboard:{doctor_id}"
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)

    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    upcoming_appointments=Appointment.query.filter_by(doctor_id=doctor_id,status="booked").all()
    patients = {appt.patient.id: {'id': appt.patient.id, 'name': appt.patient.full_name}
                for appt in appointments}
    appointment_data = [{
        'id': appt.id,
        'patient_name': appt.patient.full_name,
        'patient_id': appt.patient_id,
        'status': appt.status,
    } for appt in appointments]

    doctor = Doctor.query.get(doctor_id)

    data = {
        'doctor_name': doctor.name,
        'doctor_id': doctor.id,
        'appointments': appointment_data,
        'patients': list(patients.values())
    }
    cache.set(cache_key, data, timeout=30)
    return jsonify(data)

@doctor_bp.route("/api/doctor/<int:doctor_id>/profile", methods=["GET"])
def get_doctor_profile(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"message": "Doctor not found"}), 404

    return jsonify({
        "id": doctor.id,
        "name": doctor.name,
        "gender": doctor.gender,
        "email": doctor.email,
        "phone": doctor.phone_no,
        "department": doctor.department_name,
        "experience": doctor.experience,
    })

@doctor_bp.route("/api/doctor/<int:doctor_id>/profile", methods=["PUT"])
def update_doctor_profile(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"message": "Doctor not found"}), 404
    data = request.get_json()
    doctor.name = data.get("name", doctor.name)
    doctor.experience = data.get("experience", doctor.experience)
    doctor.gender = data.get("gender", doctor.gender)
    doctor.email = data.get("email", doctor.email)
    doctor.phone_no = data.get("phone", doctor.phone_no)
    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})


@doctor_bp.route("/api/admin/get_doctors", methods=["GET"])
def get_doctors():
    if session.get("role") != "admin":
        return jsonify({"message": "Access denied"}), 403

    doctors = Doctor.query.all()
    result = [
        {"id": d.id, "name": d.name, "email": d.email, "specialization": d.department_name}
        for d in doctors
    ]
    return jsonify(result)

@doctor_bp.route("/api/admin/get_doctor/<int:id>", methods=["GET"])
def get_doctor_by_id(id):
    if session.get("role") != "admin":
        return jsonify({"message": "Access denied"}), 403

    doctor = Doctor.query.get(id)  
    if doctor:
        result = {
            "id": doctor.id,
            "name": doctor.name,
            "email": doctor.email,
            "specialization": doctor.department_name
        }
        return jsonify({"doctor": result})
    else:
        return jsonify({"message": "Doctor not found"}), 404

@doctor_bp.route('/api/doctor/availability/<int:id>', methods=['GET'])
def get_availability(id):
    if session.get('role') != 'doctor':
        return jsonify({'message': 'Access denied'}), 403

    doctor_id = id
    today = date.today()
    next_7_days = [today + timedelta(days=i) for i in range(7)]
    for d in next_7_days:
        existing_slots = DoctorSlot.query.filter_by(
            doctor_id=doctor_id,
            date=d
        ).count()
        if existing_slots == 0:
            create_daily_slots(doctor_id, d)
    db.session.commit()
    slots = DoctorSlot.query.filter(
        DoctorSlot.doctor_id == doctor_id,
        DoctorSlot.date.in_(next_7_days)
    ).order_by(DoctorSlot.date, DoctorSlot.start_time).all()

    grouped = {}
    for s in slots:
        date_str = s.date.strftime('%d/%m/%Y')
        grouped.setdefault(date_str, []).append({
            'id': s.id,
            'start_time': s.start_time.strftime('%H:%M'),
            'end_time': s.end_time.strftime('%H:%M'),
            'status': s.status
        })

    return jsonify(grouped)


@doctor_bp.route('/api/doctor/availability/<int:id>', methods=['POST'])
def update_availability(id):
    if session.get('role') != 'doctor':
        return jsonify({'message': 'Access denied'}), 403

    data = request.json  # list of {id, date, status}

    for item in data:
        slot = DoctorSlot.query.get(item['id'])
        if slot:
            slot.status = item['status']
    db.session.commit()

    return jsonify({'success': True, 'message': 'Availability updated successfully'})


@doctor_bp.route('/api/doctor/appointment-details/<int:lookup_id>', methods=['GET'])
def get_appointment_details(lookup_id):
    """lookup_id may be appointment id (dashboard) or doctor_slot id (availability page)."""
    if session.get('role') != 'doctor':
        return jsonify({'message': 'Access denied'}), 403

    appointment = Appointment.query.get(lookup_id)
    slot = DoctorSlot.query.filter_by(appointment_id=lookup_id).first()

    if not appointment:
        slot = DoctorSlot.query.get(lookup_id)
        if not slot or not slot.appointment_id:
            return jsonify({'message': 'Appointment not found'}), 404
        appointment = Appointment.query.get(slot.appointment_id)
        if not appointment:
            return jsonify({'message': 'Appointment not found'}), 404
    elif not slot:
        slot = DoctorSlot.query.filter_by(appointment_id=appointment.id).first()

    patient = appointment.patient
    start_time = slot.start_time.strftime('%H:%M') if slot else appointment.slot.split(' - ')[0]
    end_time = slot.end_time.strftime('%H:%M') if slot else (appointment.slot.split(' - ')[1] if ' - ' in appointment.slot else '')

    return jsonify({
        'id': appointment.id,
        'status': appointment.status,
        'date': appointment.date.strftime('%Y-%m-%d'),
        'start_time': start_time,
        'end_time': end_time,
        'patient_name': patient.full_name,
        'patient_email': patient.email,
        'patient_age': patient.age,
        'patient_gender': patient.gender,
    })

@doctor_bp.route('/api/doctor/cancel-appointment/<int:appointment_id>', methods=['POST'])
def cancel_appointment_api(appointment_id):
    if session.get('role') != 'doctor':
        return jsonify({'message': 'Access denied'}), 403

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404

    appointment.status = 'cancelled'

    slot = DoctorSlot.query.filter_by(appointment_id=appointment_id).first()
    if slot:
        slot.status = 'available'
        slot.appointment_id = None

    db.session.commit()
    doctor_id = session.get('user_id')
    cache_key = f"doctor_dashboard:{doctor_id}"
    cached = cache.get(cache_key)
    if cached:
        cache.delete(cache_key)
    return jsonify({'success': True, 'message': 'Appointment cancelled'})

@doctor_bp.route('/api/doctor/mark_complete/<int:appointment_id>',methods=["POST"])
def mark_complete(appointment_id):
    if session.get('role') != 'doctor':
        return jsonify({'message': 'Access denied'}), 403
    appointment=Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    appointment.status = 'completed'
    db.session.commit()
    doctor_id = session.get('user_id')
    cache_key = f"doctor_dashboard:{doctor_id}"
    cached = cache.get(cache_key)
    if cached:
        cache.delete(cache_key)
    return jsonify({'message':'Mark as completed successfuly'})
