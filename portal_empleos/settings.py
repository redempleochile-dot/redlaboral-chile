import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# 🔐 SEGURIDAD Y ENTORNO
# =========================================================

# CLAVE SECRETA: La toma de Railway. Si no existe (local), usa una temporal.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal-desarrollo-local')

# DEBUG INTELIGENTE:
# Si existe la variable 'RAILWAY_ENVIRONMENT' (Producción), DEBUG será False (Seguro).
# Si NO existe (Tu PC), DEBUG será True (Para ver errores).
DEBUG = 'RAILWAY_ENVIRONMENT' not in os.environ

# HOSTS PERMITIDOS
ALLOWED_HOSTS = ['*', 'buscapegachile.cl', 'www.buscapegachile.cl']

# ORÍGENES DE CONFIANZA (Vital para formularios en Producción)
CSRF_TRUSTED_ORIGINS = [
    'https://buscapegachile.cl',
    'https://www.buscapegachile.cl',
    'https://redlaboral-chile-production.up.railway.app',
]

# =========================================================
# 📦 APLICACIONES INSTALADAS
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # <--- Formato de dinero y fechas
    
    # Mis Apps
    'empleos',

    # Librerías de Terceros
    'crispy_forms',
    'crispy_bootstrap5',
    'anymail',  # <--- Conector para enviar correos con Resend
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # <--- Motor de archivos estáticos
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
        conn_max_age=600
    )
}

# =========================================================
# 📧 CONFIGURACIÓN DE CORREO (RESEND 🚀)
# =========================================================

EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"

ANYMAIL = {
    "RESEND_API_KEY": os.environ.get("RESEND_API_KEY"),
}

# Identidad del correo (Esto aparecerá en el buzón del usuario)
DEFAULT_FROM_EMAIL = "Equipo Busca Pega <noreply@buscapegachile.cl>"
SERVER_EMAIL = "noreply@buscapegachile.cl"

# =========================================================
# 🎨 ARCHIVOS ESTÁTICOS Y MEDIA
# =========================================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Almacenamiento optimizado para producción
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Archivos subidos por usuarios (CVs, Logos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =========================================================
# ⚙️ OTRAS CONFIGURACIONES
# =========================================================

# Idioma y Zona Horaria
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Redirecciones de Login
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Crispy Forms (Diseño Bootstrap 5)
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'