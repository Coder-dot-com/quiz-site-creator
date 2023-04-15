"""
Django settings for quiz_site project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from decouple import config



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#set base_dir proper;y


STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS = [
    'quiz_site/static',
]

#S3 config
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY') 
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME') 

AWS_QUERYSTRING_AUTH = False #For now

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# s3 static settings
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = ''
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0'] 
#if false add allowed hosts here
ALLOWED_HOSTS.extend(
    filter(
        None,
        config('ALLOWED_HOSTS', '').split(','),
    )
)

if str(BASE_DIR) == "/APP/src":
    DEBUG = config('DEBUG', default=False, cast=bool)

    # #HTTPS settings

    USE_X_FORWARDED_HOST = True

    CSRF_TRUSTED_ORIGINS = [f"https://{x}" for x in ALLOWED_HOSTS]

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    CSRF_COOKIE_SECURE = True

    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600 # increase to 1 year eventually
    SECURE_SSL_REDIRECT = True #re enable in product
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    #With docker
    CELERY_BROKER_URL = 'redis://redis:6379'
    CELERY_RESULT_BACKEND = 'redis://redis:6379'




    STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
    STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')
    STRIPE_ENDPOINT_SECRET = config('STRIPE_ENDPOINT')


    SITE_ID = int(config('PRODUCTION_SITE_ID'))
    CURRENT_ENVIRONMENT = "production"


    DATABASES = {
    "default": {
        "ENGINE": config("SQL_ENGINE"),
        "NAME": config("SQL_DATABASE"),
        "USER": config("SQL_USER"),
        "PASSWORD": config("SQL_PASSWORD"),
        "HOST": config("SQL_HOST"),
        "PORT": config("SQL_PORT"),
    }
}

    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'




  
else:
    DEBUG = True       

    # Local
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'



    STRIPE_SECRET_KEY = config('TEST_STRIPE_SECRET_KEY')
    STRIPE_PUBLIC_KEY = config('TEST_STRIPE_PUBLIC_KEY')
    STRIPE_ENDPOINT_SECRET = config('STRIPE_ENDPOINT_SECRET')
    


    SITE_ID = int(config('LOCAL_SITE_ID'))
    CURRENT_ENVIRONMENT = "local"
    

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    STATIC_URL = 'static/'


# Email SMTP

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_SMTP_PASS') 
EMAIL_USE_TLS = True


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  
    'django.contrib.sitemaps', 
    
    'nested_admin',
    
    'blog',

    'ckeditor_uploader',

    #wagtail apps
    'wagtail',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.contrib.routable_page',

    'modelcluster',
    'taggit',
    #end wagtail

    
    'accounts',
    'session_management',
    'tinymce',
    'ckeditor',
    'emails',
    'site_settings',
    'conversion_tracking',
    'multicurrency',
    'dashboard',
    'subscriptions',
    'email_marketing',
    'landing_page',
    'colorfield',
    'tiers',
    'quiz_backend',

    'quizCreation',
    'quizRender',
    'quizPost',
    'quizData',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'quiz_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', 'src/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'site_settings.context_processors.get_site_email_logo',
                'conversion_tracking.context_processors.get_and_set_session_values',
                'multicurrency.context_processors.currency',
                'multicurrency.context_processors.user_current_currency',
                'subscriptions.context_processors.user_subscription_valid',
                'quiz_site.context_processors.main_quiz',


            ],
        },
    },
]

WSGI_APPLICATION = 'quiz_site.wsgi.application'


AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailUsernameAuthenticationBackend'
]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/







MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR /'media'
CKEDITOR_UPLOAD_PATH = 'ckeditor_uploads/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field


WAGTAIL_SITE_NAME = 'My Example Site'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Email SMTP

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_SMTP_PASS') 
EMAIL_USE_TLS = True


CKEDITOR_CONFIGS = {

'default': {
    'width': 'auto',


    'toolbar': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['TextColor', 'BGColor', 'FontSize'],
            ['Smiley'], ['Source'],
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
            ['NumberedList','BulletedList'],
            ['Indent','Outdent',],
            ], #You can change this based on your requirements.

        },
    }