from app import app,cache
from flask import Blueprint,session,jsonify
from controller.UserController import handle_login, handle_signup
from models.models import User,Doctor

routes_bp = Blueprint("auth", __name__)

@routes_bp.route('/api/login', methods=['POST'])
def login():
    return handle_login()

@routes_bp.route('/api/signup', methods=['POST'])
def signup():
    return handle_signup()

@routes_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    cache.clear() 
    return jsonify({'success': True})

@routes_bp.route('/api/me', methods=['GET'])
def me():
    user_id = session.get('user_id')
    role = session.get('role')

    if not user_id or not role:
        return jsonify({'user': None})

    if role == 'doctor':
        user = Doctor.query.get(user_id)
    else:
        user = User.query.get(user_id)

    if not user:
        return jsonify({'user': None})

    return jsonify({'user': {'email': user.email, 'role': user.role}})
