#! -*- coding: utf-8 -*-
import os
# import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd#$#5p94i$ohak3j37r*o5tw5emj!s8eva&$jsx@15lg1gsp9g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'app',
    # 'webapp',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'
WSGI_APPLICATION = 'main.wsgi.application'

# 数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
#     'default': {
#          'ENGINE': 'django.db.backends.mysql',
#          'NAME': '',
#          'USER': '',
#          'PASSWORD': '',
#          'HOST': '127.0.0.1',
#          'PORT': 3306,
#     }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'webapp/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
]

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'webapp/dist'),
    os.path.join(BASE_DIR, 'webapp/res'),
    os.path.join(BASE_DIR, 'datasettings/savepath'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

APPEND_SLASH = True

# 国际化
FILE_CHARSET= 'utf-8'
DEFAULT_CHARSET='utf-8'

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = False
USE_TZ = False

# 日志
import logging
DEFAULT_LOGGING_FILE = os.path.join(BASE_DIR, 'log/app.log')


redis_conf = {
    'host': '127.0.0.1',
    'port': 6379
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_conf['host'], redis_conf['port']),
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        },
    },
}

# # Session
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = redis_conf['host']
SESSION_REDIS_PORT = redis_conf['port']
# SESSION_REDIS_DB = 0
SESSION_REDIS_PREFIX = 'session'
# SESSION_COOKIE_AGE = 30 * 60 * 12

# Channel
CHANNEL_LAYERS = {
    # "default": {
    #     "BACKEND": "asgiref.inmemory.ChannelLayer",
    #     "ROUTING": "app.urls.channel_routing",
    # },
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_conf['host'], redis_conf['port'])],
        },
        "ROUTING": "app.urls.channel_routing",
    },
}
