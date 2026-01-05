import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# 🔐 SEGURIDAD Y DOMINIOS (¡NUEVO!)
# =========================================================

# CLAVE SECRETA (La toma de Railway o usa una por defecto local)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal-desarrollo')

# DEBUG: 'True' para ver errores detallados. En producción idealmente es 'False'.
# Lo dejamos True por ahora para que puedas ver si algo falla al lanzar.
DEBUG = True 

# 🌍 HOSTS PERMITIDOS (Quién puede visitar tu web)
ALLOWED_HOSTS = ['*', 'buscapegachile.cl', 'www.buscapegachile.cl']

# 🛡️ ORÍGENES DE CONFIANZA (Vital para que funcionen los formularios con tu dominio)
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
    'django.contrib.humanize',
    
    # Mis Apps
    'empleos',

    # Librerías de Terceros
    'crispy_forms',
    'crispy_bootstrap5',
    # 'anymail', # <--- Descomenta esto cuando instales Resend
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Carpeta de plantillas
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
# 📧 CONFIGURACIÓN DE CORREO (ACTUAL: MODO CONSOLA)
# =========================================================

# OPCIÓN ACTIVA: Muestra los correos en los LOGS de Railway (No fallan nunca)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --- FUTURO: CONFIGURACIÓN RESEND (Cuando instales la librería) ---
# Para activar esto:
# 1. Agrega 'django-anymail[resend]' a requirements.txt
# 2. Descomenta las líneas de abajo y comenta la de arriba (ConsoleBackend)

# EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"
# ANYMAIL = {
#     "RESEND_API_KEY": os.environ.get("RESEND_API_KEY"),
# }
# DEFAULT_FROM_EMAIL = "contacto@buscapegachile.cl"
# SERVER_EMAIL = "contacto@buscapegachile.cl"

# =========================================================
# 🎨 ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES)
# =========================================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Motor de almacenamiento eficiente para Railway
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Configuración de Archivos Multimedia (Subida de CVs y Logos)
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

# Login
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Crispy Forms (Para que los formularios se vean bonitos)
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'