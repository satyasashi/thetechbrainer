import os
import json
from decouple import Config, RepositoryEnv
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


with open('secrets.json') as f:
    secrets = json.loads(f.read())


def get_secret_key(setting, secrets=secrets):
    '''Get the secret variable or return explicit exception.'''
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(setting)
    raise ImproperlyConfigured(error_msg)

# SECURITY WARNING: keep the secret key used in production secret!
# DOTENV_FILE = os.path.join(BASE_DIR, 'keys.env')
# env_config = Config(RepositoryEnv(DOTENV_FILE))


# use the Config().get() method as you normally would since
# decouple.config uses that internally.
# i.e. config('SECRET_KEY') = env_config.get('SECRET_KEY')
SECRET_KEY = get_secret_key("SECRET_KEY")


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # AWS S3
    #'storages',

    # our apps

    'blog.apps.BlogConfig',
    'siteuser.apps.SiteuserConfig',
    'toolbelt.apps.ToolbeltConfig',

    # third party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    # 'thumbnails',
    'ckeditor',
    'ckeditor_uploader',

    # providers
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'thetechbrainer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'blog.processors.get_recent_posts_side_box',
                'blog.processors.check_if_moderator_has_notifications',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'thetechbrainer.wsgi.application'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SITE_ID = 1

#AUTH_USER_MODEL = 'account.Account'

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/accounts/login/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[No Reply]: Thetechbrainer.com: "
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_BLACKLIST = ["admin", "root", "test", "administrator", "moderator", "editor"]
ACCOUNT_USERNAME_MIN_LENGTH = 2


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

IMG_SMALL = (140, 98)

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }

# THUMBNAILS = {
#     'METADATA': {
#         'BACKEND': 'thumbnails.backends.metadata.DatabaseBackend',
#     },
#     'STORAGE': {
#         'BACKEND': 'thetechbrainer.storage_backends.MediaStorage',
#         # You can also use Amazon S3 or any other Django storage backends
#     },
#     'SIZES': {
#         'small': {
#             'PROCESSORS': [
#                 {'PATH': 'thumbnails.processors.resize', 'width': 10, 'height': 10},
#                 {'PATH': 'thumbnails.processors.crop', 'width': 80, 'height': 80}
#             ],
#             'POST_PROCESSORS': [
#                 {
#                     'processor': 'thumbnails.post_processors.optimize',
#                     'png_command': 'optipng -force -o7 "%(filename)s"',
#                     'jpg_command': 'jpegoptim -f --strip-all "%(filename)s"',
#                 },
#             ],
#         },
#         'large': {
#             'PROCESSORS': [
#                 {'PATH': 'thumbnails.processors.resize', 'width': 20, 'height': 20},
#                 {'PATH': 'thumbnails.processors.flip', 'direction': 'horizontal'}
#             ],
#         }
#     }
# }

# EMAIL SETTINGS
SERVER_EMAIL = get_secret_key("ADMIN_EMAIL2")
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = get_secret_key('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = SERVER_EMAIL
EMAIL_PORT = 587
# EMAIL_SUBJECT_PREFIX = "[No Reply]: Thetechbrainer"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMINS = [
    (get_secret_key("ADMIN_NAME"), get_secret_key("ADMIN_EMAIL")),
    (get_secret_key("ADMIN_NAME2"), get_secret_key("ADMIN_EMAIL2")),
]

MANAGERS = ADMINS

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

CKEDITOR_JQUERY_URL = "https://code.jquery.com/jquery-3.5.1.min.js"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 800,
        'extraPlugins': ','.join({'codesnippet', 'image2'}),
        'stylesSet': [
            {
                "name": 'content',
                "element": 'textarea',
                "attributes": {'class': 'save'},
            },
        ],
    },

    'awesome_ckeditor': {
        'toolbar': 'full',
        'height': 300,
        'width': 1000,
        'extraPlugins': ','.join({'codesnippet'})
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static_files')
]


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

