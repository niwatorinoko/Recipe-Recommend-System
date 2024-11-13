import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# templatesフォルダーのパス
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
# mediaフォルダーのパス
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# staticフォルダーのパス
STATIC_DIR = os.path.join(BASE_DIR, 'static')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-629%$p!$*c=4-8e&9xad-*w@=&ptgh_17rp1p+7wgr8ww26q79'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    
    'recipe',
    'authentications',
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

ROOT_URLCONF = 'reciperecommendsystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR], # templatesフォルダーのパスを指定
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

WSGI_APPLICATION = 'reciperecommendsystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    STATIC_DIR,
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL='authentications.User'


# SANITY_PROJECT_ID = os.getenv("SANITY_PROJECT_ID", "gv2vw359")
# SANITY_DATASET = os.getenv("SANITY_DATASET", "production")
# SANITY_API_TOKEN = os.getenv("SANITY_API_TOKEN", "skgyQBp24zvw9klAaafbN2ZFfVtC5EqLTBes4Clz2dM4j9INLhinLCx6ccIxWDktM4s9FcQHIIa60DdGWBRi5VF003JoLFxa8vf3kDjnSxRGYz3K9vPB1CEAW34WDv1kSRvKjFyndMKt6IKddXl0kf3OWrPhYYEBi2LzUGQmwfMedjdus2jL")
# SANITY_API_VERSION = "v2023-11-12"  # 使用する API バージョン


# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

import environ

# instanceを作成
env = environ.Env(
    # 初期値を設定
    DEBUG=(bool, False)
)

# manage.pyのある階層にある.envを読み込む
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# .envのSECRET_KEYをSECRET_KEYに代入
GOOGLE_API_KEY = env('GOOGLE_API_KEY')