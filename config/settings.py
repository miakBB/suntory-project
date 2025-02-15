"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "default-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]


# Application definition
#アプリケーション達 上記6個はデフォルトで設定されている
INSTALLED_APPS = [
    'django.contrib.admin', #デフォルトの管理画面
    'django.contrib.auth', #デフォルトのログイン等
    'django.contrib.contenttypes', #デフォルトのコンテンツタイプ
    'django.contrib.sessions', #デフォルトのセッション
    'django.contrib.messages', #デフォルトのメッセージ
    'django.contrib.staticfiles', #デフォルトの静的ファイル
    'users', #ユーザー登録、ログイン、ユーザー更新
    'dashboard',#ダッシュボード　サマリ画面
    'records',#飲料の記録登録、閲覧
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], #テンプレートディレクトリの指定
        'APP_DIRS': True, #アプリケーションのテンプレートディレクトリを検索する
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = "users.User"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

#パスワードの禁止事項(現在デフォルト)

AUTH_PASSWORD_VALIDATORS = [ 
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', #ユーザーと似たパスワード禁止
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', #最小文字数指定
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', #一般的なパスワード禁止
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', #数字のみのパスワード禁止
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ja'

LOGIN_URL = '/users/login/'

LOGIN_REDIRECT_URL = '/dashboard/'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/" #静的ファイルのディレクトリ指定(プロジェクト直下)

STATICFILES_DIRS = (
    [
        os.path.join(BASE_DIR, "static"), 
    ]
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
