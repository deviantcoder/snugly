from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY', cast=str)

DEBUG = config('DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = []


# Email config

DOMAIN = config('DOMAIN', cast=str, default='http://127.0.0.1:8000')

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', cast=str, default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', cast=str, default='587')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str, default='jamessullivanpost@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', cast=str)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool, default=False)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps

    'crispy_forms',
    'crispy_bootstrap5',

    # apps
    
    'accounts.apps.AccountsConfig',
    'users.apps.UsersConfig',
    'mentors.apps.MentorsConfig',
    'managers.apps.ManagersConfig',
    'commands.apps.CommandsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 3rd party

    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# Auth config

AUTH_USER_MODEL = 'accounts.AppUser'

# Logging config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG', # or INFO
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/debug.log',
        }
    },
    'loggers': {
        'accounts.models': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False, # could be True
        },
    },
}

# Crispy forms

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True


# Static files

STATIC_URL = 'static/'

STATICFILES_BASE_DIR = BASE_DIR / 'static'
STATICFILES_BASE_DIR.mkdir(exist_ok=True, parents=True)

STATICFILES_VENDOR_DIR = STATICFILES_BASE_DIR / 'vendor'

STATICFILES_DIRS = [
    STATICFILES_BASE_DIR
]

STATIC_ROOT = 'local_cdn'


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
