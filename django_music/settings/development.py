from .base import *

DEBUG = True
STATICFILES_DIRS = (BASE_DIR / 'staticfiles',)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'