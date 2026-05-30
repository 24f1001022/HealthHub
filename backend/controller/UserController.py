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
    session["user_id"] = user.id
    session['role'] = user.role 
    return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
        }), 200

def handle_signup():
    data= request.json
    if not data or not data.get('email') or not data.get('Full_name') or not data.get('password') or not data.get('Address') or not data.get('Age') or not data.get('Gender'):
        return jsonify({'message': "Please Fill All The Details"}), 400
    if data.get('password') != data.get('confirm_password'):
        return jsonify({'message': 'Password Mismatch'}), 401
    email=data.get('email')
    password=data.get('password')
    full_name=data.get('Full_name')
    age=data.get('Age')
    gender=data.get('Gender')
    address=data.get('Address')
    phone_no=data.get('PhoneNo')
    user=User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'User already exist with this email'}), 401
    user=User(email=email,password=password,full_name=full_name,address=address,age=age,gender=gender,phone_no=phone_no)
    db.session.add(user)
    db.session.commit()
    from tasks import send_welcome_email_task
    from email_utils import send_welcome_email
    try:
        send_welcome_email_task.delay(email)
    except Exception:
        try:
            send_welcome_email(email)
        except Exception:
            pass
    return jsonify({"success": True,'message': 'Account created Sucessfully'}), 200