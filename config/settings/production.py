"""
Production settings for English Learning App Backend.
"""
from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")

SECRET_KEY = os.environ.get("SECRET_KEY")

# قاعدة البيانات
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# ملفات static
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

