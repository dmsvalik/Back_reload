import os
from datetime import timedelta
from pathlib import Path

import environ
from celery.schedules import crontab


env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent

FONT_DIR = os.path.join(BASE_DIR, 'fonts')
ttf_file = os.path.join(FONT_DIR, 'Montserrat-Medium.ttf')
PDF_DIR = os.path.join(BASE_DIR, 'media/pdf_storage')
design_pdf = os.path.join(PDF_DIR, 'designpdf.pdf')

environ.Env.read_env()
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env("SECRET_KEY", default="SOME_SECRET_KEY")

DEBUG = env("DEBUG_STATUS", default=False)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "whywe.ru",
    "*"
]

CSRF_TRUSTED_ORIGINS = [
    "http://app",
    "http://185.244.173.82",
    "https://api.whywe.ru",
]

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework.authtoken",
    "app.main_page",
    "app.products",
    "app.orders",
    "app.utils",
    "app.chat",
    "app.users",
    "rest_framework",
    "djoser",
    "drf_yasg",
    "debug_toolbar",
    "corsheaders",
    "app.tests",
    'drf_api_logger',
    "channels",
    "app.questionnaire",
    "app.sending",
]

DOMAIN = ("api.whywe.ru")

SITE_NAME = ("whywe.ru")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
]

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://localhost:3000",
    "http://app",
    "http://185.244.173.82",
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://app:8000",
    "http://app",
    "http://185.244.173.82:8000",
]


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
INTERNAL_IPS = [
    "127.0.0.1",
]

# Daphne
ASGI_APPLICATION = "config.asgi.application"

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

# Chats
CHATTING = {
    'LIST_MESSAGE_LIMIT': 1,
    'DAYS_TO_UNLOCK': 1,
}

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": env("POSTGRES_DB", default="whywe"),
        "USER": env("POSTGRES_USER", default="whywe"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="whywe"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default=5432),
    }
}

# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#     EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

EMAIL_HOST = env("EMAIL_HOST", default="email_host")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="email_host_user")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="email_pass")
EMAIL_PORT = env("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=True)

# yandex-disk token
TOKEN = env("TOKEN", default="TOKEN")

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "app/main_page/static")]

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '2000/day',
        'user': '2000/day',
    },

}

# Documentation https://djoser.readthedocs.io/en/latest/settings.html
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#jwk-url

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=720),
    "BLACKLIST_AFTER_ROTATION": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

}

DJOSER = {
    "LOGIN_FIELD": "email",
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "SET_USERNAME_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "USERNAME_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "EMAIL": {
        "activation": "app.users.email.Activation",
        "confirmation": "app.users.email.Confirmation",
        # 'password_reset': 'main_page.email.PasswordReset',
        # 'password_changed_confirmation': 'main_page.email.PasswordChangedConfirmation',
        "username_reset": "app.users.email.UsernameReset",
        # 'username_reset_confirmation': 'main_page.email.UsernameResetConfirmation',
    },
    "SERIALIZERS": {
        "user_create": "app.users.serializers.UserCreateSerializer",
        "user": "app.users.serializers.UserAccountSerializer",
        "current_user": "app.users.serializers.UserAccountSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
    "PERMISSIONS": {
        "user_list": ["djoser.permissions.CurrentUserOrAdmin"],
        "set_email": ["djoser.permissions.CurrentUserOrAdmin"],
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

AUTH_USER_MODEL = "users.UserAccount"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "DEFAULT_AUTO_SCHEMA_CLASS": "drf_yasg.inspectors.SwaggerAutoSchema",
}

SWAGGER_TAGS = {
    "files": "Работа с файлами",
    "order": "Работа с заказами",
    "offer": "Офферы",
    "users": "Аккаунт пользователя",
    "users_service": "Методы авторизованного пользователя",
    "auth": "Авторизация",
    "service": "Сервисные функции",
    "contractor": "Исполнитель"
}

MAX_SERVER_QUOTA = 5 * 1024 * 1024
MAX_STORAGE_QUOTA = 10 * 1024 * 1024
MAX_ORDERS = 50

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://localhost:6379/0")
CELERY_BEAT_SCHEDULE = {
    "check_expired_auction_orders": {
        "task": "utils.views.check_expired_auction_orders",
        "schedule": crontab(minute="0", hour="*/12"),
    },
}

# записывать логи
# документация https://pypi.org/project/drf-api-logger/
DRF_API_LOGGER_DATABASE = True
# максимум 50 записей держит в кэше до записи в таблицу
DRF_LOGGER_QUEUE_MAX_SIZE = 50
# максимум раз в десять секунд пишет в таблицу
DRF_LOGGER_INTERVAL = 10
# плюс 180 минут к UTС часовой пояс мск
DRF_API_LOGGER_TIMEDELTA = 180
# формат ссылки на ручку
DRF_API_LOGGER_PATH_TYPE = 'FULL_PATH'
# регистрируемые статусы сейчас все, можно отрегулировать
# DRF_API_LOGGER_STATUS_CODES = ['400', '401', '403', '404', '405', '500', '503']
# Отслеживаем медленные команды
DRF_API_LOGGER_SLOW_API_ABOVE = 200

SENDING = {
    "DISABLE_URL": "disable_notifications/{uid}/{token}/"
}

ORDER_COOKIE_KEY_NAME = "key"
