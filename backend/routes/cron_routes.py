"""HTTP cron hooks for scheduled emails (use free cron-job.org on Render free tier)."""
from flask import Blueprint, request, jsonify
import config
from tasks import run_daily_appointment_reminder, run_monthly_doctor_report

cron_bp = Blueprint('cron', __name__)


def _authorized():
    secret = request.headers.get('X-Cron-Secret') or request.args.get('secret', '')
    return config.CRON_SECRET and secret == config.CRON_SECRET


@cron_bp.route('/api/cron/daily-reminders', methods=['POST'])
def cron_daily_reminders():
    if not _authorized():
        return jsonify({'error': 'Unauthorized'}), 401
    result = run_daily_appointment_reminder()
    return jsonify({'ok': True, 'result': result})


@cron_bp.route('/api/cron/monthly-reports', methods=['POST'])
def cron_monthly_reports():
    if not _authorized():
        return jsonify({'error': 'Unauthorized'}), 401
    result = run_monthly_doctor_report()
    return jsonify({'ok': True, 'result': result})
