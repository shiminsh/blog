"""
Django settings for blog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import join
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from configurations import Configuration, values

class Common(Configuration):

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '5g!dwg_u7&!7&d%^y7gq%wrm_b*&xr*c#h54lnxy$n-7-v_un='

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    TEMPLATE_DEBUG = True

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',

        )

    ALLOWED_HOSTS = []


    # Application definition

    DJANGO_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    THIRD_PARTY_APPS = (
        'south',
        'tinymce',
        'django_wysiwyg',
        )

    LOCAL_APPS = (
        'blogging',
        )

    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'config.urls'

    WSGI_APPLICATION = 'config.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/

    STATIC_URL = '/static/'
    
    STATICFILES_DIRS = (
        ('assets', join(BASE_DIR, 'static')),
    )

    STATIC_ROOT = join(BASE_DIR, 'blogging/static')

    TEMPLATE_DIRS = (
        join(BASE_DIR, 'templates'),
    )

    MEDIA_URL = '/media/'

    MEDIA_ROOT = join(BASE_DIR, 'media')

    DJANGO_WYSIWYG_MEDIA_URL = '/media/'

    DJANGO_WYSIWYG_FLAVOR = "tinymce_advanced"

    LOGIN_REDIRECT_URL = '/accounts/loggedin/'

class Local(Common):

    # DEBUG
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    # INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    # END INSTALLED_APPS

    # MAIL settigs
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')
    # End mail settings

    # django-debug-toolbar
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    # end django-debug-toolbar


class Production(Common):
    
    # INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    # End INSTALLED_APPS

    # django-secure
    INSTALLED_APPS += ("djangosecure",)
