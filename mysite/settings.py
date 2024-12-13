import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv("mysite/database.env")
print("Database Name:", os.getenv("DATABASE_NAME"))
print("Database User:", os.getenv("DATABASE_USER"))
print("Database Host:", os.getenv("DATABASE_HOST"))
print("Database Port:", os.getenv("DATABASE_PORT"))


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-p=owv8y(&-%z!5_$88kl7ezp+zh$r1w@a#wsfyg4q!9_=oscgh"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to False in production

ALLOWED_HOSTS = [
    "django-tutorial-test-before-deploy.eba-uh8yfpf2.us-west-2.elasticbeanstalk.com",
    "127.0.0.1",
    "localhost",
    "*",
]  # Add your domain or server IP in production


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "rentals.apps.RentalsConfig",
    # 'django.contrib.admin',          # Django admin interface
    "django.contrib.auth",  # Authentication framework
    "django.contrib.contenttypes",  # Content types framework
    "django.contrib.sessions",  # Session framework
    "django.contrib.messages",  # Messaging framework
    "django.contrib.staticfiles",  # Static files handling
    # Your custom apps
    "users",  # App for user registration/authentication
    # 'groups',                        # App for posting messages in groups (if applicable)
    "roommates",
    "discussions",
    "chatbot",
    "storages",
    "alerts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rentals.middleware.LoginRequiredMiddleware",
]

ROOT_URLCONF = "mysite.urls"  # The main URL configuration file

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # Custom template directory
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

WSGI_APPLICATION = "mysite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# Default database is SQLite. For production, use PostgreSQL, MySQL, etc.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("RDS_DB_NAME"),
        "USER": os.getenv("RDS_USERNAME"),
        "PASSWORD": os.getenv("RDS_PASSWORD"),
        "HOST": os.getenv("RDS_HOSTNAME"),
        "PORT": os.getenv("RDS_PORT"),
        "OPTIONS": {
            "options": "-c timezone=utc",
        },
        "TEST": {
            "NAME": "test_ebdb-new-pooja",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"  # Default language

TIME_ZONE = "UTC"  # Adjust for your timezone

USE_I18N = True  # Enable internationalization

USE_L10N = True  # Enable localization

USE_TZ = True  # Enable timezone support

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = "us-west-2"

# Use S3 for media storage
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"  # Base URL for serving static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # Where static files are located

# Media files (user-uploaded content like profile pics)
MEDIA_URL = "https://us-west-2.console.aws.amazon.com/s3/buckets/elasticbeanstalk-us-west-2-682033502272?region=us-west-2&bucketType=general&prefix=django-tutorial-test-before-deploy2/media/"
MEDIA_ROOT = "https://us-west-2.console.aws.amazon.com/s3/buckets/elasticbeanstalk-us-west-2-682033502272?region=us-west-2&bucketType=general&prefix=django-tutorial-test-before-deploy2/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Authentication settings
AUTH_USER_MODEL = "users.User"  # Custom user model (if you're using one)
LOGIN_REDIRECT_URL = "home"  # Redirect to home after login
LOGOUT_REDIRECT_URL = "home"  # Redirect to home after logout

# Email backend for sending email (e.g., verification)
# For development, you can use the console backend:
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"  # Logs emails to console
)
# In production, you’d configure a real email backend here (SMTP, etc.)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Log out when the browser is closed
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session expiry with each request
USE_TZ = False

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # Or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "rentsense2024@gmail.com"  # Your email
EMAIL_HOST_PASSWORD = "ehrhqehcerudmkds"  # Your email password or app-specific password
DEFAULT_FROM_EMAIL = "rentsense2024@gmail.com"
