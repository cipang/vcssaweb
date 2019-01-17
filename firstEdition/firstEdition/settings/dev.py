from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2sqj10c9trd1+(0&_zuhx2)eh#7&@w_=b3#&xpaip1z$e3^z#m'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[Wagtail] '
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'vcssatest@gmail.com'
EMAIL_HOST_PASSWORD = 'vcssaadmin'

EMAIL_PORT = 587
EMAIL_USE_TLS = True

try:
    from .local import *
except ImportError:
    pass
