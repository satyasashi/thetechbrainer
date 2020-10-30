from thetechbrainer.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS += ['www.thetechbrainer.com']

DATABASES = {
    'default': get_secret_key("PROD_DATABASE"),
}
