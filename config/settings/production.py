"""
Production settings for English Learning App Backend.
"""
from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")

SECRET_KEY = os.environ.get("SECRET_KEY")



DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=True,
        default='postgres://postgres:1234@127.0.0.1:5432/elb'
    )
}

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

# ملفات static

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

