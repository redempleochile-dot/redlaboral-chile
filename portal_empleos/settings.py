import os
from pathlib import Path
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Construcción de rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# SEGURIDAD E INFRAESTRUCTURA (CORREGIDO)
# =========================================================

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal-desarrollo')

# IMPORTANTE: Cambia esto a False una vez que confirmes que el Admin funciona
DEBUG = True 

ALLOWED_HOSTS = ['*']

# 👇 ESTAS 3 LÍNEAS ARREGLAN EL ERROR DEL ADMIN (CSRF) 👇
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True  # Fuerza a todos a usar HTTPS (Candado seguro)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Confianza en los dominios de Railway
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app', 'https://*.up.railway.app']

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
    'django.contrib.humanize',  # Para formatos de fecha y moneda
    
    # LIBRERÍAS DE NUBE (Orden importante)
    'cloudinary_storage',
    'cloudinary',
    
    'empleos', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
# BASE DE DATOS
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
# ARCHIVOS ESTÁTICOS Y CORREO
# =========================================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email en consola para evitar errores 500 si no hay servidor real
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================================================
# CONFIGURACIÓN INTELIGENTE DE CLOUDINARY
# =========================================================

CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

if CLOUDINARY_URL:
    # 1. Parsear la URL larga que nos da Railway (cloudinary://Key:Secret@CloudName)
    try:
        # Quitamos el prefijo
        url_body = CLOUDINARY_URL.replace("cloudinary://", "")
        # Separamos credenciales del nombre de la nube
        creds_part, cloud_name = url_body.split("@")
        # Separamos Key y Secret
        api_key, api_secret = creds_part.split(":")

        # 2. Configurar el Almacenamiento (Para subir archivos)
        CLOUDINARY_STORAGE = {
            'CLOUD_NAME': cloud_name,
            'API_KEY': api_key,
            'API_SECRET': api_secret,
        }
        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
        
        # 3. Configurar la Librería General (Para que funcionen los templates y no salga el error de cloud_name)
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
    except Exception as e:
        print(f"Error configurando Cloudinary: {e}")
        # Si Django necesita redirigir al login y no sabe dónde, usa esto:
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/'  # Al entrar, mandar a la portada
LOGOUT_REDIRECT_URL = '/' # Al salir, mandar a la portada