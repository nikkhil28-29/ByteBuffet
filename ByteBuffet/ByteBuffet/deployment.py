# import os 
# from .settings import *
# from .settings import BASE_DIR


# SECRET_KEY = os.environ['SECRET']
# ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
# CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
# DEBUG = False

# # WhiteNoise configuration
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',

#     'whitenoise.middleware.WhiteNoiseMiddleware',
# ] 

# # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STORAGES = {
#     # ...
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

# conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
# conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': conn_str_params['dbname'],
#         'HOST': conn_str_params['host'],
#         'USER': conn_str_params['user'],
#         'PASSWORD': conn_str_params['password'],
#     }
# }


import os
from .settings import *  # Import base settings from settings.py
from pathlib import Path

# Secret key and allowed hosts from environment variables
SECRET_KEY = os.environ['SECRET']  # This must be set in your Azure environment variables
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]  # Azure's app service hostname
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]  # For CSRF protection

# Debug should be turned off for production
DEBUG = False

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Middleware configuration including WhiteNoise for serving static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static file handling
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Collect static files here during deployment

# WhiteNoise settings for static file compression and caching in production
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",  # Compressed static files
    },
}

# Additional directories to look for static files (development)
STATICFILES_DIRS = [
    BASE_DIR / 'ByteBuffet/static',  # Your static directory for local development
]

# Media files (uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Directory for user-uploaded files

# Azure PostgreSQL database configuration
conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']  # Get connection string from environment
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conn_str_params['dbname'],  # Database name
        'HOST': conn_str_params['host'],  # Database host
        'USER': conn_str_params['user'],  # Database user
        'PASSWORD': conn_str_params['password'],  # Database password
        'PORT': '5432',  # PostgreSQL default port (optional if using the default)
    }
}

# Ensure secure connection (optional)
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
SESSION_COOKIE_SECURE = True  # Ensure cookies are sent over HTTPS
CSRF_COOKIE_SECURE = True  # Ensure CSRF cookies are sent over HTTPS

# Logging configuration for Azure (optional, can be customized as needed)
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'error.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }



aiodns==3.2.0
aiosmtpd==1.4.5
asgiref==3.8.1
atpublic==4.1.0
attrs==23.2.0
cffi==1.16.0
Django==5.0.4
Django-Verify-Email==2.0.3
dnspython==2.6.1
email_validator==2.1.1
idna==3.6
pillow==10.3.0
psycopg2==2.9.9
pycares==4.4.0
pycparser==2.22
python-dotenv==1.0.1
python-slugify==8.0.4
slugify==0.0.1
sqlparse==0.5.0
text-unidecode==1.3
typing_extensions==4.11.0
verify-email==2.4.3
# GDAL==3.2.2
verify_email==2.4.3
python_dotenv==1.0.1
rest_framework_simplejwt==0.0.2
email_validator==2.2.0
slugify==0.0.1
Pillow==10.4.0
psycopg2==binary==2.9.9
simplejson==3.19.3
whitenoise==6.7.0 