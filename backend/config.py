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

# Flask-Mail (Gmail: use App Password — spaces are stripped automatically)
def _clean_mail(value):
    if not value:
        return None
    return value.strip().strip('"').strip("'").replace(' ', '')


MAIL_SERVER        = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT          = int(os.getenv('MAIL_PORT', '587'))
MAIL_USE_TLS       = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
MAIL_USERNAME      = os.getenv('MAIL_USERNAME', '').strip().strip('"').strip("'") or None
MAIL_PASSWORD      = _clean_mail(os.getenv('MAIL_PASSWORD'))
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER') or MAIL_USERNAME
MAIL_SUPPRESS_SEND = os.getenv('MAIL_SUPPRESS_SEND', 'False').lower() == 'true'

# Celery (disabled on Render free — no background workers)
USE_CELERY = os.getenv('USE_CELERY', 'false').lower() == 'true'

# Cron endpoints (daily/monthly emails via cron-job.org)
CRON_SECRET = os.getenv('CRON_SECRET', '')

# Redis + Session — must be redis:// or rediss:// (NOT the Upstash REST https URL)
def _valid_redis_url(url: str) -> bool:
    if not url:
        return False
    return url.startswith(('redis://', 'rediss://', 'unix://'))


def _pick_redis_url() -> str:
    # Upstash dashboard labels: "Redis URL" → use that, not "REST URL"
    for key in ('REDIS_URL', 'UPSTASH_REDIS_URL'):
        raw = os.getenv(key, '').strip().strip('"').strip("'")
        if _valid_redis_url(raw):
            return raw
    return ''


REDIS_URL = _pick_redis_url()
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
    SESSION_FILE_DIR = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'flask_session')
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