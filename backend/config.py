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

# Celery (disabled on Render free — no background workers)
USE_CELERY = os.getenv('USE_CELERY', 'false').lower() == 'true'

# Cron endpoints (daily/monthly emails via cron-job.org)
CRON_SECRET = os.getenv('CRON_SECRET', '')

# Redis + Session (optional — falls back to filesystem if REDIS_URL unset)
REDIS_URL = os.getenv('REDIS_URL', '').strip()
USE_REDIS = bool(REDIS_URL)

SESSION_PERMANENT  = True
SESSION_USE_SIGNER = False
SESSION_KEY_PREFIX = os.getenv('SESSION_KEY_PREFIX', 'flask_session:')

if USE_REDIS:
    SESSION_TYPE = 'redis'
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = REDIS_URL
else:
    SESSION_TYPE = 'filesystem'
    CACHE_TYPE = 'SimpleCache'

# Public URLs (production)
PUBLIC_BASE_URL = os.getenv('PUBLIC_BASE_URL', 'http://localhost:5000').rstrip('/')
FRONTEND_URL    = os.getenv('FRONTEND_URL', 'http://localhost:5173').rstrip('/')

# Misc
EXPORT_FOLDER = os.path.join(os.getcwd(), 'exports')
FLASK_ENV     = os.getenv('FLASK_ENV', 'development')

# Cross-origin sessions (Vercel frontend + Render API)
_is_prod = FLASK_ENV == 'production'
SESSION_COOKIE_SAMESITE = 'None' if _is_prod else 'Lax'
SESSION_COOKIE_SECURE   = _is_prod