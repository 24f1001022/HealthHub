import os
from dotenv import load_dotenv

load_dotenv()

# Secret
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')

# Database — swap postgres:// → postgresql:// for SQLAlchemy
_db_url = os.getenv('DATABASE_URL', 'sqlite:///hospital.db')
if _db_url.startswith('postgres://'):
    _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
SQLALCHEMY_DATABASE_URI = _db_url
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Mail
MAIL_SERVER   = os.getenv('MAIL_SERVER',   'smtp.gmail.com')
MAIL_PORT     = int(os.getenv('MAIL_PORT', '587'))
MAIL_USE_TLS  = os.getenv('MAIL_USE_TLS',  'True').lower() == 'true'
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

# Redis + Session
REDIS_URL           = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
SESSION_TYPE        = os.getenv('SESSION_TYPE', 'redis')
SESSION_PERMANENT   = True
SESSION_USE_SIGNER  = False
SESSION_KEY_PREFIX  = os.getenv('SESSION_KEY_PREFIX', 'flask_session:')
SESSION_COOKIE_SECURE   = os.getenv('FLASK_ENV') == 'production'
SESSION_COOKIE_SAMESITE = 'Lax'

# Cache
CACHE_TYPE      = 'RedisCache'
CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Misc
EXPORT_FOLDER = os.path.join(os.getcwd(), 'exports')
FLASK_ENV     = os.getenv('FLASK_ENV', 'development')