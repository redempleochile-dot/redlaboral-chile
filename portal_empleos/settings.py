import os
from pathlib import Path

# Construye las rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD: En producción real esto debería ser una variable de entorno
SECRET_KEY = 'django-insecure-cambiar-esta-clave-por-seguridad-en-produccion'

# IMPORTANTE: Dejamos DEBUG=True para ver errores en tu primera prueba. 
# Cuando formalices la empresa, esto se cambia a False.
DEBUG = True

# Permitir cualquier host (Necesario para Render/Nube)
ALLOWED_HOSTS = ['*']

# --- APLICACIONES INSTALADAS ---
INSTALLED_APPS = [
    'jazzmin',                      # <--- PANEL ADMINISTRATIVO (Va primero)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps de Utilidad
    'django.contrib.humanize',      # Formato de números ($ 1.000)
    'django.contrib.sitemaps',      # SEO para Google
    
    # Tu Aplicación Principal
    'empleos',
]

# --- MIDDLEWARE (Intermediarios de seguridad y carga) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <--- CRÍTICO PARA LA NUBE (Estilos CSS)
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
        'DIRS': [], # Django busca en las carpetas 'templates' de cada app
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

# --- BASE DE DATOS ---
# Usamos SQLite por defecto (ideal para prototipo inicial)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- VALIDACIÓN DE CONTRASEÑAS ---
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# --- INTERNACIONALIZACIÓN (CHILE) ---
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# --- ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES DEL SISTEMA) ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Compresión para la nube (WhiteNoise)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- ARCHIVOS MULTIMEDIA (SUBIDOS POR USUARIOS: CV, FOTOS, VIDEOS) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- REDIRECCIONES DE LOGIN ---
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# --- EMAIL (Simulado en consola para desarrollo) ---
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURACIÓN VISUAL JAZZMIN (PANEL EJECUTIVO) ---
JAZZMIN_SETTINGS = {
    "site_title": "Red Laboral Admin",
    "site_header": "Red Laboral Chile",
    "site_brand": "Panel Ejecutivo",
    "welcome_sign": "Bienvenido al Centro de Control",
    "copyright": "Red Laboral Chile SpA",
    "search_model": "auth.User",
    "topmenu_links": [
        {"name": "Ver Sitio Web", "url": "home", "permissions": ["auth.view_user"]},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "empleos.OfertaLaboral": "fas fa-briefcase",
        "empleos.Candidato": "fas fa-user-graduate",
        "empleos.PerfilEmpresa": "fas fa-building",
        "empleos.Postulacion": "fas fa-file-signature",
        "empleos.Notificacion": "fas fa-bell",
        "empleos.ReporteOferta": "fas fa-exclamation-triangle",
        "empleos.Pregunta": "fas fa-comments",
        "empleos.Favorito": "fas fa-heart",
        "empleos.AlertaEmpleo": "fas fa-envelope-open-text",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-danger",
    "accent": "accent-danger",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-danger",
    "sidebar_nav_small_text": False,
    "theme": "flatly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}