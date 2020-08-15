from thetechbrainer.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS += ['www.thetechbrainer.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'db_config.cnf'),
        }
    }
}
