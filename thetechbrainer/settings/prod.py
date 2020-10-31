from thetechbrainer.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS += ['www.thetechbrainer.com', '206.189.129.28', 'localhost', 'thetechbrainer.com']

DATABASES = {
    'default': get_secret_key("PROD_DATABASE"),
}
