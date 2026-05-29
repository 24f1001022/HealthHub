from flask import Blueprint, jsonify, session,request
from models.models import User,db,Department,Doctor,Appointment,PatientTreatment,DoctorSlot
from app import cache

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/api/admin/dashboard", methods=["GET"])
def admin_dashboard():
    if session.get("role") != "admin":
        return jsonify({"message": "Access denied"}), 403

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "User ID not found in session"}), 400

    cache_key = "admin_dashboard"

    cached_data = cache.get(cache_key)
    if cached_data:
        return jsonify(cached_data)
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    patients_data = User.query.filter_by(role='patient').all()
    appointment_data = Appointment.query.filter_by(status='booked').all()
    doctors_data = Doctor.query.all()
    data = {
        "admin_name": user.full_name.capitalize(),
        "doctors": [{"id": d.id, "name": d.name} for d in doctors_data],
        "patients": [{"id": p.id, "name": p.full_name} for p in patients_data],
        "appointments": [
            {"id": a.id,"patient": a.patient.full_name,"doctor": a.doctor.name,"department": a.doctor.department_name,} for a in appointment_data],
    }

    cache.set(cache_key, data, timeout=30)
    return jsonify(data)

@admin_bp.route("/api/admin/add_doctor", methods=["POST"])
def add_doctor():
    if session.get("role") != "admin":
        return jsonify({"message": "Access denied"}), 403
    data = request.json
    try:
        name = data.get("name")
        experience = data.get("experience")
        email = data.get("email")
        gender = data.get("gender")
        phone_no = data.get("phone_no")
        password = data.get("password")
        department_name = data.get("department")
        department = Department.query.filter_by(dpt_name=department_name).first()
        if not department:
            return jsonify({"message": "Department not found"}), 400
        if Doctor.query.filter_by(email=email).first():
            return jsonify({"message": "Doctor with this email already exists"}), 400

        doctor = Doctor(
            name=name,
            department_name=department_name,
            experience=experience,
            email=email,
            gender=gender,
            phone_no=phone_no,
            role="doctor",
            dpt_id=department.id,
        )
        doctor.password = password

        db.session.add(doctor)
        db.session.commit()
        cache.delete("admin_dashboard")

        return jsonify({"success": True, "message": "Doctor added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        print("Error adding doctor:", e)
        return jsonify({"success": False, "message": str(e)}), 500

@admin_bp.route('/api/admin/add_department', methods=['POST'])
def add_department():
    data = request.json
    dpt_name = data.get('dpt_name')
    description = data.get('description')

    if not dpt_name:
        return jsonify({"success": False, "message": "Department name is required"}), 400

    existing = Department.query.filter_by(dpt_name=dpt_name).first()
    if existing:
        return jsonify({"success": False, "message": "Department already exists"}), 409

    try:
        new_department = Department(dpt_name=dpt_name, description=description)
        db.session.add(new_department)
        db.session.commit()
        return jsonify({"success": True, "message": "Department added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
@admin_bp.route("/api/admin/delete_doctor/<int:doctor_id>", methods=["DELETE"])
def delete_doctor(doctor_id):
    if session.get("role") != "admin":
        return jsonify({"message": "Access denied"}), 403

    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({"success": False, "message": "Doctor not found"}), 404
        booked = Appointment.query.filter_by(doctor_id=doctor_id, status="booked").all()
        if booked:
            return jsonify({
                "success": False,
                "message": "Doctor cannot be deleted because booked appointments exist."
            }), 400
        non_booked = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status != "booked"
        ).all()
        for appt in non_booked:
            PatientTreatment.query.filter_by(appointment_id=appt.id).delete()
            db.session.delete(appt)
        DoctorSlot.query.filter_by(doctor_id=doctor_id).delete()
        db.session.delete(doctor)
        db.session.commit()
        if cache.get("admin_dashboard"):
            cache.delete("admin_dashboard")

        return jsonify({"success": True, "message": "Doctor deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print("Error deleting doctor:", e)
        return jsonify({"success": False, "message": str(e)}), 500

@admin_bp.route("/api/admin/delete_patient/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    if session.get("role") != "admin":
        return jsonify({"message": "Access denied"}), 403
    try:
        patient = User.query.get(patient_id)
        if not patient:
            return jsonify({"success": False, "message": "Patient not found"}), 404

        appointments = Appointment.query.filter_by(patient_id=patient.id).all()
        for appt in appointments:
            slot = DoctorSlot.query.filter_by(appointment_id=appt.id).first()
            if slot:
                slot.status = "available"
                slot.appointment_id = None
        PatientTreatment.query.filter_by(patient_id=patient.id).delete()
        for appt in appointments:
            db.session.delete(appt)
        db.session.delete(patient)
        db.session.commit()
        cache.delete("admin_dashboard")

        return jsonify({"success": True, "message": "Patient deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        print("Error deleting patient:", e)
        return jsonify({"success": False, "message": str(e)}), 500
