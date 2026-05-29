# routes/export_routes.py
from flask import Blueprint, request, jsonify,send_from_directory
import os
from redis import Redis

export_bp= Blueprint("export_bp", __name__)
r = Redis.from_url('redis://localhost:6379/0')


@export_bp.route("/api/patient/<int:patient_id>/export-treatments", methods=["POST"])
def trigger_export(patient_id):
    data = request.get_json()
    email = data.get("email")

    from tasks import export_patient_treatments_task  
    task = export_patient_treatments_task.delay(patient_id, email)
    return jsonify({
        "message": "Export started",
        "task_id": task.id,
        "status_url": f"/api/patient/{patient_id}/export-status/{task.id}"
    }), 202


@export_bp.route("/api/patient/<int:patient_id>/export-status/<task_id>", methods=["GET"])
def get_export_status(patient_id, task_id):
    key = f"export:{patient_id}:{task_id}"
    data = r.hgetall(key)
    if not data:
        return jsonify({"status": "unknown"}), 200

    decoded = {k.decode(): v.decode() for k, v in data.items()}
    return jsonify(decoded), 200

@export_bp.route('/exports/<path:filename>')
def download_export(filename):
    exports_folder = os.path.join(os.getcwd(), 'exports')
    return send_from_directory(exports_folder, filename, as_attachment=True)