import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# 🔐 SEGURIDAD Y ENTORNO
# =========================================================

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal-desarrollo-local')

# DEBUG INTELIGENTE: False en Railway (Producción), True en tu PC.
DEBUG = 'RAILWAY_ENVIRONMENT' not in os.environ

ALLOWED_HOSTS = ['*', 'buscapegachile.cl', 'www.buscapegachile.cl']

CSRF_TRUSTED_ORIGINS = [
    'https://buscapegachile.cl',
    'https://www.buscapegachile.cl',
    'https://redlaboral-chile-production.up.railway.app',
]

# =========================================================
# 📦 APLICACIONES INSTALADAS
# =========================================================

INSTALLED_APPS = [
    # 👑 Jazzmin debe ir ANTES de 'django.contrib.admin'
    'jazzmin',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Utilidades Django
    'django.contrib.humanize',  # Formato de dinero y fechas
    'django.contrib.sites',     # Necesario para "Olvidé mi contraseña"
    
    # Mis Apps
    'empleos',

    # Librerías de Terceros
    'crispy_forms',
    'crispy_bootstrap5',
    'anymail',  # Envío de correos
]

# ID del sitio (Vital para que funcionen los enlaces de correos)
SITE_ID = 1

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
# 🗄️ BASE DE DATOS (PostgreSQL)
# =========================================================

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3', 
        conn_max_age=600
    )
}

# =========================================================
# 👑 CONFIGURACIÓN DE JAZZMIN (El nuevo Dashboard)
# =========================================================

JAZZMIN_SETTINGS = {
    "site_title": "Admin Busca Pega",
    "site_header": "Busca Pega Chile",
    "site_brand": "Busca Pega Chile",
    "welcome_sign": "Bienvenido al Panel de Control",
    "copyright": "Busca Pega Chile SpA",
    "search_model": "auth.User",
    
    # Menú lateral
    "show_sidebar": True,
    "navigation_expanded": True,
    
    # Iconos para tus modelos (Opcional, se ve bonito)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "empleos.Oferta": "fas fa-briefcase", # Ajusta si tu modelo se llama distinto
        "empleos.Empresa": "fas fa-building",
    },
}

# Tema visual del admin (Puedes probar otros como 'flatly', 'darkly', etc.)
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly", 
    "dark_mode_theme": "darkly",
}

# =========================================================
# 📧 CORREO (Resend)
# =========================================================

EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"

ANYMAIL = {
    "RESEND_API_KEY": os.environ.get("RESEND_API_KEY"),
}

DEFAULT_FROM_EMAIL = "Equipo Busca Pega <noreply@buscapegachile.cl>"
SERVER_EMAIL = "noreply@buscapegachile.cl"

# =========================================================
# 🎨 ARCHIVOS ESTÁTICOS Y MEDIA
# =========================================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =========================================================
# ⚙️ OTRAS CONFIGURACIONES
# =========================================================

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'