import os
from pathlib import Path
import dj_database_url

# Construcción de rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# SEGURIDAD E INFRAESTRUCTURA
# =========================================================

# Clave secreta: Intenta leerla de Railway, si no, usa una por defecto para local
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal-desarrollo')

# DEBUG = 'RAILWAY_ENVIRONMENT' not in os.environ  <-- BORRA O COMENTA ESTA
DEBUG = 'RAILWAY_ENVIRONMENT' not in os.environ

# Hosts permitidos: Acepta todo para evitar problemas en la nube
ALLOWED_HOSTS = ['*']

# Orígenes confiables (Importante para el Login en Railway)
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']

# =========================================================
# APLICACIONES INSTALADAS
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    'cloudinary_storage',
    'cloudinary',
    'empleos', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <--- MOTOR DE ARCHIVOS ESTÁTICOS
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
        # 👇 AQUÍ ESTÁ LA CORRECCIÓN DEL ERROR 500 👇
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
# BASE DE DATOS (POSTGRESQL + SQLITE)
# =========================================================

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3', 
        conn_max_age=600
    )
}

# =========================================================
# VALIDADORES DE CONTRASEÑA
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# =========================================================
# IDIOMA Y ZONA HORARIA
# =========================================================

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# =========================================================
# ARCHIVOS ESTÁTICOS Y MEDIA
# =========================================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# =========================================================
# CONFIGURACIÓN DE CORREO (MODO PRUEBA)
# =========================================================

# Esto hace que los correos NO se envíen, sino que aparezcan en el Log de Railway.
# ¡Es perfecto para arreglar el Error 500 sin configurar Gmail todavía!
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# =========================================================
# ALMACENAMIENTO EN LA NUBE (CLOUDINARY)
# =========================================================

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Decirle a Django que use esto para guardar archivos (CVs, Fotos)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'