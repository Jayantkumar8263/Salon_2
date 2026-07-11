from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv())


SECRET_KEY = 'django-insecure-4@53h(#6x07h!rt74lio&$%qe4ue^wb!fus+30&fz(y2#aov!8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [ 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'salon_app',
    'owner',
    'customer_app',
    'Staff_app',
    'rest_framework', 
    'rest_framework.authtoken',
    'storages',
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

ROOT_URLCONF = 'Salon_2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Salon_2.wsgi.application'



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Rds Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database-1',
        'USER': 'postgres',
        'PASSWORD': 'Aws_12345',
        'HOST': 'database-1.c5se6sg0oxmq.ap-south-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

#STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'

#MEDIA_URL = '/media/'# this is the URL for media files, used when you want to access media files in templates
MEDIA_ROOT = BASE_DIR / 'media' # this is the path where media files are stored on the server, used when you want to save media files uploaded by users


# Django REST Framework configuration

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ]
}

# S3 bucket configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

# NEW: Additional S3 settings for modern AWS buckets
AWS_S3_OBJECT_PARAMETERS = { # is line me humne S3 object parameters set kiye hain, 'CacheControl': 'max-age=86400' ka matlab hai ki hum apne S3 object ko 1 day ke liye cache karenge, cache matlab ki agar koi user same object ko dobara request karega to wo cache se serve hoga instead of S3 bucket se, isse performance improve hoti hai aur S3 requests kam hoti hain.
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_VERIFY = True
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
# MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
# Static files (CSS, JavaScript, Images)
# Use 'storages.backends.s3.S3Storage' for Django >= 4.2
# Use 'storages.backends.s3boto3.S3Boto3Storage' for older versions

STORAGES = {
    "default": {
        "BACKEND": "salon_app.storage_backends.MediaStorage",
    },
    "staticfiles": {
        "BACKEND": "salon_app.storage_backends.StaticStorage",
    },
}

# STORAGES = {
#     "default": {
#         "BACKEND": "django.core.files.storage.FileSystemStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     },
# }

STATIC_URL = '/static/'
MEDIA_URL = '/media/'