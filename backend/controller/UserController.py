from models.models import User,db,Doctor
from flask import jsonify,request,session

def handle_login():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing email or password"}), 400
    email = data["email"]
    password = data["password"]
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        user=Doctor.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"message": "Invalid credentials"}), 401
    session.permanent = True
    session['user_id'] = user.id
    session['role'] = user.role
    session.modified = True
    return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
        }), 200

def _send_welcome_email_background(email):
    """Do not block signup HTTP response (avoids Vercel 502 on slow SMTP)."""
    import threading
    from app import app

    def _run():
        with app.app_context():
            from email_utils import send_welcome_email
            import config
            try:
                if config.USE_CELERY:
                    from tasks import send_welcome_email_task
                    send_welcome_email_task.delay(email)
                else:
                    send_welcome_email(email)
            except Exception as exc:
                print(f'Welcome email failed for {email}: {exc}')

    threading.Thread(target=_run, daemon=True).start()


def handle_signup():
    data = request.json or {}
    required = ('email', 'Full_name', 'password', 'Address', 'Gender', 'PhoneNo')
    missing = [k for k in required if not data.get(k) and data.get(k) != 0]
    if 'Age' not in data or data.get('Age') in (None, ''):
        missing.append('Age')
    if missing:
        return jsonify({'success': False, 'message': 'Please fill all required fields'}), 400

    if data.get('password') != data.get('confirm_password'):
        return jsonify({'success': False, 'message': 'Passwords do not match'}), 400

    email = data.get('email', '').strip().lower()
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'An account with this email already exists'}), 400

    gender = data.get('Gender')
    if gender == 'M':
        gender = 'Male'
    elif gender == 'F':
        gender = 'Female'

    try:
        age = int(data.get('Age'))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Age must be a number'}), 400

    user = User(
        email=email,
        password=data.get('password'),
        full_name=data.get('Full_name'),
        address=data.get('Address'),
        age=age,
        gender=gender,
        phone_no=str(data.get('PhoneNo')),
    )
    db.session.add(user)
    db.session.commit()

    _send_welcome_email_background(email)
    return jsonify({'success': True, 'message': 'Account created successfully'}), 200