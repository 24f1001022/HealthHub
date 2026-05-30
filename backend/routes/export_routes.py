# routes/export_routes.py
import os
import uuid
from flask import Blueprint, request, jsonify, send_from_directory
import config
from tasks import export_patient_treatments_sync, _get_redis

export_bp = Blueprint('export_bp', __name__)


def _decode_status(data):
    if not data:
        return None
    return {k.decode(): v.decode() for k, v in data.items()}


@export_bp.route('/api/patient/<int:patient_id>/export-treatments', methods=['POST'])
def trigger_export(patient_id):
    data = request.get_json() or {}
    email = data.get('email')
    task_id = str(uuid.uuid4())

    if config.USE_CELERY:
        from tasks import export_patient_treatments_task
        task = export_patient_treatments_task.delay(patient_id, email)
        return jsonify({
            'message': 'Export started',
            'task_id': task.id,
            'status_url': f'/api/patient/{patient_id}/export-status/{task.id}',
        }), 202

    filepath, task_id = export_patient_treatments_sync(patient_id, email, task_id)
    return jsonify({
        'message': 'Export complete',
        'task_id': task_id,
        'status': 'finished',
        'filepath': filepath,
        'status_url': f'/api/patient/{patient_id}/export-status/{task_id}',
    }), 200


@export_bp.route('/api/patient/<int:patient_id>/export-status/<task_id>', methods=['GET'])
def get_export_status(patient_id, task_id):
    key = f'export:{patient_id}:{task_id}'
    r = _get_redis()
    if r:
        data = _decode_status(r.hgetall(key))
        if data:
            return jsonify(data), 200
    return jsonify({'status': 'unknown'}), 200


@export_bp.route('/exports/<path:filename>')
def download_export(filename):
    exports_folder = os.path.join(os.getcwd(), 'exports')
    return send_from_directory(exports_folder, filename, as_attachment=True)
