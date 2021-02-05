from thetechbrainer.settings.base import *

INSTALLED_APPS += [
    # dev tools apps
    'debug_toolbar',
    'django_extensions',
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


INTERNAL_IPS = [
    '127.0.0.1',
]

DATABASES = {
    'default': get_secret_key("DEV_DATABASE")
}
