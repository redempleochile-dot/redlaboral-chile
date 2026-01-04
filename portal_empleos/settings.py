import os
from pathlib import Path
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Construcción de rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# 🔐 SEGURIDAD E INFRAESTRUCTURA
# =========================================================

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal')

# AUTOMÁTICO: Si estamos en Railway (Producción), DEBUG será False. En tu PC, será True.
# (Asegúrate de no tener el typo 'os.environs', es 'os.environ')
DEBUG = True

ALLOWED_HOSTS = ['*']

# SOLUCIÓN AL ERROR CSRF (403) Y HTTPS
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app', 'https://*.up.railway.app', 'https://*.redlaboral.cl'] # Agregué tu dominio futuro por si acaso
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# REDIRECCIONES DE LOGIN (Público)
LOGIN_URL = 'login'           
LOGIN_REDIRECT_URL = 'home'   
LOGOUT_REDIRECT_URL = 'home'  

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
    'django.contrib.sitemaps', 
    'django.contrib.humanize', 
    
    # NUBE (Orden importante)
    'cloudinary_storage',
    'cloudinary',
    
    'empleos', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # Motor de archivos estáticos
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
# 🗄️ BASE DE DATOS (PostgreSQL en Railway)
# =========================================================

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3', 
        conn_max_age=600,
        ssl_require=True 
    )
}

# Solo para desarrollo local (si no hay DATABASE_URL)
if 'DATABASE_URL' not in os.environ:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

# =========================================================
# 🌐 IDIOMA Y ZONA
# =========================================================

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# =========================================================
# 📂 ARCHIVOS ESTÁTICOS Y MEDIA
# =========================================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================================================
# 📧 CONFIGURACIÓN DE CORREO (VUELTA AL PUERTO 587 - TLS)
# =========================================================

# =========================================================
# 📧 CONFIGURACIÓN DE CORREO (TRUCO GOOGLEMAIL)
# =========================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# 👇 CAMBIO MÁGICO: Usamos este host para evitar error IPv6
EMAIL_HOST = 'smtp.googlemail.com' 

EMAIL_PORT = 587
EMAIL_USE_TLS = True    # TLS Encendido
EMAIL_USE_SSL = False   # SSL Apagado

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# =========================================================
# ☁️ CLOUDINARY (Imágenes)
# =========================================================

CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

if CLOUDINARY_URL:
    try:
        # Lógica para leer la URL larga de Railway
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