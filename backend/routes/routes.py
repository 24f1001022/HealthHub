from flask import jsonify, Blueprint
from models.models import Department, User

general_bp = Blueprint("general", __name__)


@general_bp.route("/health", methods=["GET"])
@general_bp.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@general_bp.route("/api/departments", methods=["GET"])
def get_departments():
    depts = Department.query.all()
    return jsonify([{"id": d.id, "dpt_name": d.dpt_name} for d in depts])

@general_bp.route("/api/get_patients", methods=["GET"])
def get_patients():
    patients = User.query.filter_by(role='patient').all()
    return jsonify( [{"id": p.id, "name": p.full_name} for p in patients])
