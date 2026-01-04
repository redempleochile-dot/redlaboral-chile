import os
from pathlib import Path
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Construcción de rutas
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# 🔐 SEGURIDAD E INFRAESTRUCTURA
# =========================================================

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal')

# EN PRODUCCIÓN: Cambia esto a False cuando confirmes que todo está estable
DEBUG = 'RAILWAY_ENVIRONMENT' not in os.environ

ALLOWED_HOSTS = ['*']

# SOLUCIÓN AL ERROR CSRF (403) EN RAILWAY
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app', 'https://*.up.railway.app']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# REDIRECCIONES DE LOGIN (Público)
LOGIN_URL = 'login'           # Nombre de la ruta en urls.py
LOGIN_REDIRECT_URL = 'home'   # A dónde ir al entrar
LOGOUT_REDIRECT_URL = 'home'  # A dónde ir al salir

# =========================================================
# 📦 APLICACIONES
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps', # Para SEO
    'django.contrib.humanize', # Para formatos ($ 1.000)
    
    # NUBE
    'cloudinary_storage',
    'cloudinary',
    
    'empleos', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # Motor de archivos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portal_empleos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'portal_empleos.wsgi.application'

# =========================================================
# 🗄️ BASE DE DATOS
# =========================================================

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3', 
        conn_max_age=600
    )
}

# =========================================================
# 🌐 IDIOMA Y ZONA
# =========================================================

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# =========================================================
# 📂 ARCHIVOS Y MEDIA
# =========================================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =========================================================
# 📧 CONFIGURACIÓN DE CORREO (VERSIÓN SSL BLINDADA)
# =========================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'

# 👇 CAMBIO CLAVE: Usamos puerto 465 y SSL
EMAIL_PORT = 465
EMAIL_USE_TLS = False   # <--- Apagamos TLS
EMAIL_USE_SSL = True    # <--- Prendemos SSL

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# =========================================================
# ☁️ CLOUDINARY (Solución Definitiva)
# =========================================================

CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

if CLOUDINARY_URL:
    try:
        # Lógica para parsear la URL de Railway
        url_body = CLOUDINARY_URL.replace("cloudinary://", "")
        creds_part, cloud_name = url_body.split("@")
        api_key, api_secret = creds_part.split(":")

        CLOUDINARY_STORAGE = {
            'CLOUD_NAME': cloud_name,
            'API_KEY': api_key,
            'API_SECRET': api_secret,
        }
        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
        
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
    except Exception as e:
        print(f"⚠️ Error configurando Cloudinary: {e}")