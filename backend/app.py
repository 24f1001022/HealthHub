from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_session import Session
from flask_caching import Cache
from models.models import db, User

app = Flask(__name__)
app.config.from_pyfile('config.py')

_frontend = app.config.get('FRONTEND_URL', 'http://localhost:5173')
_cors_origins = list({_frontend, 'http://localhost:5173', 'http://127.0.0.1:5173'})
CORS(app, supports_credentials=True, origins=_cors_origins)
mail = Mail(app)

if app.config.get('USE_REDIS'):
    from redis import Redis
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    cache = Cache(app, config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': app.config['REDIS_URL'],
    })
else:
    app.redis = None
    cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

Session(app)

db.init_app(app)

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            email='admin@admin.com',
            password='admin',
            full_name='admin',
            role='admin',
            age=99,
            phone_no='9999999999',
        )
        db.session.add(admin)
        db.session.commit()

from routes.auth_routes import routes_bp
from routes.patient_routes import patient_bp
from routes.doctor_routes import doctor_bp
from routes.admin_routes import admin_bp
from routes.routes import general_bp
from routes.export_routes import export_bp
from routes.cron_routes import cron_bp

app.register_blueprint(export_bp)
app.register_blueprint(cron_bp)
app.register_blueprint(routes_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(general_bp)

import models

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
