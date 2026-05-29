from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_session import Session
from flask_caching import Cache
from redis import Redis
from models.models import db,User

app = Flask(__name__)
CORS(app,supports_credentials=True)
app.config.from_pyfile('config.py')
mail = Mail(app)

app.redis = Redis.from_url(app.config['REDIS_URL'])
Session(app)
cache = Cache(app, config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': app.config['REDIS_URL']
})

db.init_app(app)

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(email='admin@admin.com',password='admin',full_name='admin',role='admin',age=99,phone_no='9999999999')
        db.session.add(admin)
        db.session.commit()

from routes.auth_routes import routes_bp
from routes.patient_routes import patient_bp
from routes.doctor_routes import doctor_bp
from routes.admin_routes import admin_bp
from routes.routes import general_bp 
from routes.export_routes import export_bp
app.register_blueprint(export_bp)
app.register_blueprint(routes_bp,)
app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(general_bp)

import models

if __name__ == "__main__":
    app.run(debug=True,host='localhost', port=5000)
