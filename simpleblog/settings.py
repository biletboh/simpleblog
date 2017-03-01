import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#-s&xl0!*$rs1tu%!3(xqm1k%7fyk-4e!bet5v@casbft*w)-('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # handle email confirmation 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # handle images
    'easy_thumbnails',
    
    # django file form
    'django_file_form',
    'django_file_form.ajaxuploader',
    
    # template widgets
    'widget_tweaks',

    # datetime widget
    'datetimewidget',

    # tinyMCE full text editor
    'tinymce',

    # ajax pagination
    'el_pagination',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simpleblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'simpleblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases


CURRDB = {'ENGINE': 'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}

DATABASES = {
    'default': CURRDB
    }


if DEBUG is False:
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)



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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# allauth configuration

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_USERNAME_REQUIRED = True 
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = 'simpleblog.noreply@gmail.com'
EMAIL_HOST_PASSWORD = 'nosorog999'
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Simple Blog. '

LOGIN_REDIRECT_URL = '/'

# thumbnails configuration

THUMBNAIL_DEFAULT = STATIC_URL + 'blog/img/' + 'noimage.png'
THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (100, 100), 'crop': True},
        'thumb': {'size': (200, 200), 'crop': True},
        'small': {'size': (250, 250), 'crop': True},
        'medium': {'size': (750, 400), 'crop': True},
        'large': {'size': (800, 550), 'crop': True},
        'extra_large': {'size': (1200, 600), 'crop': True},
    },
}

#TinyMCE config
TINYMCE_JS_URL = '/static/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = '/static/tiny_mce'

TINYMCE_DEFAULT_CONFIG = {
        'plugins': 'advlist,autolink,autoresize,emotions,fullpage,fullscreen,media,table,paste,searchreplace,wordcount',
        'theme': "advanced",
        'theme_advanced_resizing': True,
        'theme_advanced_resize_horizontal': True,
        'theme_advanced_buttons1': 'undo,redo,fontselect,fontsizeselect,bold,italic,underline,strikethrough,|,forecolor,backcolor,|,bullist,numlist,|,justifyleft,justifycenter,justifyright,justifyfull,|,outdent,indent,|,link,unlink,|,emotions,blockquote,|,table,hr,sub,sup,charmap',
        'theme_advanced_buttons2' : "",
        'width': '100%',
        'cleanup_on_startup': True,
        'custom_undo_redo_levels': 10,
        }
TINYMCE_COMPRESSOR = False 
TINYMCE_FILEBROWSER = False 

# el pagination configuration

EL_PAGINATION_PER_PAGE = 2
