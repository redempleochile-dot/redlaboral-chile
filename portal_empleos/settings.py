import os
from pathlib import Path
import dj_database_url  # Importante para PostgreSQL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# CONFIGURACIÓN DE SEGURIDAD
# =========================================================

# CLAVE SECRETA: Intenta leerla de Railway, si no hay, usa una por defecto para desarrollo
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal-desarrollo')

# DEBUG: En Railway debe ser False (producción), en tu PC True.
# Si la variable 'RAILWAY_ENVIRONMENT' existe, asume producción.
DEBUG = 'RAILWAY_ENVIRONMENT' not in os.environ

# HOSTS PERMITIDOS: Acepta todo para evitar el error "DisallowedHost"
ALLOWED_HOSTS = ['*']

# ORIGENES CONFIABLES (Para evitar problemas con el Login en HTTPS)
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']

# =========================================================
# APLICACIONES
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Tus aplicaciones (Asegúrate de que el nombre coincida con tus carpetas)
    'empleos',  # <--- CONFIRMA QUE ESTE ES EL NOMBRE DE TU APP
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <--- ESENCIAL PARA RAILWAY
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portal_empleos.urls' # <--- CONFIRMA EL NOMBRE DE TU PROYECTO

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # Puedes poner [os.path.join(BASE_DIR, 'templates')] si usas carpeta global
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

WSGI_APPLICATION = 'portal_empleos.wsgi.application' # <--- CONFIRMA EL NOMBRE

# =========================================================
# BASE DE DATOS (EL CORAZÓN ROBUSTO) 🐘
# =========================================================

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3', # En tu PC usa esto
        conn_max_age=600    # Mantiene la conexión viva para rapidez
    )
}

# =========================================================
# VALIDACIÓN DE CONTRASEÑAS
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

LANGUAGE_CODE = 'es-cl'  # Español Chile
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# =========================================================
# ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES)
# =========================================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración de WhiteNoise para servir archivos comprimidos y cacheados
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Para subir imágenes (Perfil, Currículums, etc)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =========================================================
# AUTO FIELD
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'