from .base import *

DEBUG = False
STATIC_ROOT = BASE_DIR / 'staticfiles'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'