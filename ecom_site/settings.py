import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Security and debug from environment
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-for-prod')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS can be provided via comma-separated env var, or fall back to Render host
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', os.environ.get('RENDER_EXTERNAL_HOSTNAME', '*')).split(',')

# Use BigAutoField by default to avoid auto-created primary key warnings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'shop',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecom_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom_site.wsgi.application'

# Database configuration
# Prefer DATABASE_URL (e.g., from Render Postgres). Falls back to MySQL if
# MYSQL_DB is set, otherwise to local sqlite for development.
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    try:
        import dj_database_url
    except ImportError:
        raise ImproperlyConfigured(
            "DATABASE_URL is set but the 'dj-database-url' package is not installed."
        )

    # 1. Parse the configuration from the URL
    db_config = dj_database_url.config(default=DATABASE_URL, conn_max_age=600)

    # 2. Fix the 'ssl-mode' vs 'ssl_mode' issue for MySQL
    if db_config.get('ENGINE') == 'django.db.backends.mysql':
        if 'OPTIONS' not in db_config:
            db_config['OPTIONS'] = {}
        
        # If dj_database_url added 'ssl-mode', rename it to 'ssl_mode'
        if 'ssl-mode' in db_config['OPTIONS']:
            db_config['OPTIONS']['ssl_mode'] = db_config['OPTIONS'].pop('ssl-mode')

        # If an ssl CA is provided via env vars, write it to a temp file
        # and set `OPTIONS['ssl'] = {'ca': <path>}` so DB drivers that
        # expect an `ssl` dict will use it. This mirrors the logic used
        # for the `MYSQL_DB` branch above.
        if 'ssl_mode' in db_config['OPTIONS']:
            ssl_ca_path = None
            if os.environ.get('MYSQL_SSL_CA'):
                ssl_ca_path = os.environ.get('MYSQL_SSL_CA')
            elif os.environ.get('MYSQL_SSL_CA_BASE64'):
                import base64
                import tempfile

                ca_b64 = os.environ.get('MYSQL_SSL_CA_BASE64')
                try:
                    ca_bytes = base64.b64decode(ca_b64)
                    tmp = tempfile.NamedTemporaryFile(delete=False)
                    tmp.write(ca_bytes)
                    tmp.flush()
                    ssl_ca_path = tmp.name
                except Exception:
                    ssl_ca_path = None

            if ssl_ca_path and 'ssl' not in db_config['OPTIONS']:
                db_config['OPTIONS']['ssl'] = {'ca': ssl_ca_path}

            # Remove `ssl_mode` to avoid passing unsupported kwargs to
            # certain MySQL drivers (they will use `ssl` dict instead).
            db_config['OPTIONS'].pop('ssl_mode', None)
    DATABASES = {
        'default': db_config
    }
else:
    MYSQL_DB = os.environ.get('MYSQL_DB')
    if MYSQL_DB:
            # Support Aiven-style MySQL connections that require an SSL CA.
            # You can provide the CA as a file path in `MYSQL_SSL_CA`, or as
            # a base64-encoded string in `MYSQL_SSL_CA_BASE64` (recommended
            # for Render environment variables). If neither is provided the
            # connection will proceed without an explicit CA file.
            ssl_ca_path = None
            if os.environ.get('MYSQL_SSL_CA'):
                ssl_ca_path = os.environ.get('MYSQL_SSL_CA')
            elif os.environ.get('MYSQL_SSL_CA_BASE64'):
                import base64
                import tempfile

                ca_b64 = os.environ.get('MYSQL_SSL_CA_BASE64')
                try:
                    ca_bytes = base64.b64decode(ca_b64)
                    tmp = tempfile.NamedTemporaryFile(delete=False)
                    tmp.write(ca_bytes)
                    tmp.flush()
                    ssl_ca_path = tmp.name
                except Exception:
                    ssl_ca_path = None

            options = {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            }
            if ssl_ca_path:
                options['ssl'] = {'ca': ssl_ca_path}

            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': MYSQL_DB,
                    'USER': os.environ.get('MYSQL_USER', 'ecom_user'),
                    'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
                    'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
                    'PORT': os.environ.get('MYSQL_PORT', '3306'),
                    'OPTIONS': options,
                }
            }
    else:
        # Fallback to a local sqlite database for easy local development
        import warnings

        warnings.warn(
            'No DATABASE_URL or MYSQL_DB set; falling back to SQLite for local development.',
            RuntimeWarning,
        )

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-IN'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
CORS_ALLOW_ALL_ORIGINS = True

# Include the project-level `static/` folder so runserver can serve CSS/JS in DEBUG
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
CORS_ALLOW_ALL_ORIGINS = True

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files storage (WhiteNoise for static assets)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Optional S3-backed media (set USE_S3=True and AWS_* env vars in Render)
if os.environ.get('USE_S3', 'False') == 'True':
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')