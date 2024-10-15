import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p=owv8y(&-%z!5_$88kl7ezp+zh$r1w@a#wsfyg4q!9_=oscgh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to False in production

ALLOWED_HOSTS = ['django-env.eba-gvvxnxg6.us-east-2.elasticbeanstalk.com']  # Add your domain or server IP in production


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',          # Django admin interface
    'django.contrib.auth',           # Authentication framework
    'django.contrib.contenttypes',   # Content types framework
    'django.contrib.sessions',       # Session framework
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static files handling

    # Your custom apps
    'users'                         # App for user registration/authentication
    #'groups',                        # App for posting messages in groups (if applicable)

    # Additional third-party apps can be added here if needed
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

ROOT_URLCONF = 'mysite.urls'  # The main URL configuration file

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Custom template directory
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# Default database is SQLite. For production, use PostgreSQL, MySQL, etc.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Using SQLite for development
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'  # Default language

TIME_ZONE = 'UTC'  # Adjust for your timezone

USE_I18N = True  # Enable internationalization

USE_L10N = True  # Enable localization

USE_TZ = True  # Enable timezone support


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'  # Base URL for serving static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Where static files are located

# Media files (user-uploaded content like profile pics)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication settings
AUTH_USER_MODEL = 'users.User'  # Custom user model (if you're using one)
LOGIN_REDIRECT_URL = 'home'  # Redirect to home after login
LOGOUT_REDIRECT_URL = 'home'  # Redirect to home after logout

# Email backend for sending email (e.g., verification)
# For development, you can use the console backend:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Logs emails to console
# In production, you’d configure a real email backend here (SMTP, etc.)
