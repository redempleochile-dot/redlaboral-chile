import os
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# --- FUNCIONES AUXILIARES (NO BORRAR - Requeridas por historial de migraciones) ---

def renombrar_foto(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('fotos_candidatos/', filename)

def renombrar_logo(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('logos_empresas/', filename)

def renombrar_banner(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('banners_empresas/', filename)

def renombrar_archivo(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/', filename)

def validar_video(value):
    filesize = value.size
    limit = 50 * 1024 * 1024 # 50MB
    if filesize > limit:
        raise ValidationError("El tamaño máximo del archivo es de 50MB.")

# --- OPCIONES GLOBALES ---
REGIONES_CHILE = [
    ('AP', 'Arica y Parinacota'), ('TA', 'Tarapacá'), ('AN', 'Antofagasta'), 
    ('AT', 'Atacama'), ('CO', 'Coquimbo'), ('VA', 'Valparaíso'), 
    ('RM', 'Metropolitana'), ('BI', 'O’Higgins'), ('MA', 'Maule'), 
    ('NB', 'Ñuble'), ('BI', 'Biobío'), ('AR', 'Araucanía'), 
    ('LR', 'Los Ríos'), ('LS', 'Los Lagos'), ('AI', 'Aysén'), 
    ('MA', 'Magallanes')
]

NIVEL_EXPERIENCIA = [
    ('sin_experiencia', 'Sin experiencia'), 
    ('junior', 'Junior (1-2 años)'), 
    ('semi_senior', 'Semi Senior (3-5 años)'), 
    ('senior', 'Senior (+5 años)')
]

TIPO_TRABAJO = [
    ('full_time', 'Full Time'), 
    ('part_time', 'Part Time'), 
    ('freelance', 'Freelance'), 
    ('practica', 'Práctica Profesional'), 
    ('remoto', '100% Remoto'),
    ('hibrido', 'Híbrido'),
    ('PRA', 'Práctica Profesional') 
]

RUBROS_CHILE = [
    ('admin', 'Administración y Oficina'), ('agro', 'Agricultura y Pesca'), 
    ('arte', 'Arte y Diseño'), ('comercio', 'Comercio y Ventas'), 
    ('construccion', 'Construcción y Obras'), ('educacion', 'Educación'), 
    ('gastronomia', 'Gastronomía y Turismo'), ('salud', 'Salud y Medicina'), 
    ('tecnologia', 'Tecnología e Informática'), ('transporte', 'Transporte y Logística'), 
    ('otro', 'Otros Oficios')
]

# --- MODELOS ---

class PerfilEmpresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_empresa')
    nombre = models.CharField(max_length=150, verbose_name="Nombre de la Empresa", blank=True, null=True)
    logo = models.ImageField(upload_to=renombrar_logo, blank=True, null=True)
    banner = models.ImageField(upload_to=renombrar_banner, blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    es_destacada = models.BooleanField(default=False)
    es_premium = models.BooleanField(default=False)
    
    # 🔴 CORREGIDO: Usamos default=timezone.now para evitar error de migración
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self): return self.nombre or self.usuario.username

class OfertaLaboral(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ofertas', null=True, blank=True)
    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200, blank=True, null=True)
    tipo = models.CharField(max_length=50, choices=TIPO_TRABAJO)
    duracion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Duración del contrato")
    modalidad = models.CharField(max_length=50, choices=[('Presencial', 'Presencial'), ('Remoto', 'Remoto'), ('Hibrido', 'Híbrido')], default='Presencial')
    region = models.CharField(max_length=50, choices=REGIONES_CHILE)
    experiencia = models.CharField(max_length=50, choices=NIVEL_EXPERIENCIA, default='sin_experiencia')
    sueldo = models.IntegerField(blank=True, null=True, verbose_name="Sueldo Líquido (Opcional)")
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    fecha_cierre = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono / WhatsApp")
    wsp_activo = models.BooleanField(default=False, verbose_name="¿Contactar por WhatsApp?")
    email_contacto = models.EmailField(blank=True, null=True)
    etiquetas = models.CharField(max_length=200, blank=True, null=True, help_text="Ej: Python, Ventas, Licencia B")
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to=renombrar_archivo, blank=True, null=True)
    publicada = models.BooleanField(default=False)
    pagada = models.BooleanField(default=False)
    es_destacado = models.BooleanField(default=False)
    visitas = models.IntegerField(default=0)

    def __str__(self): return self.titulo

class Candidato(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidato', null=True, blank=True)
    nombre = models.CharField(max_length=200)
    titular = models.CharField(max_length=200, verbose_name="Titular Profesional", help_text="Ej: Ingeniero Comercial, Gasfiter Certificado")
    rubro = models.CharField(max_length=50, choices=RUBROS_CHILE, default='otro')
    foto = models.ImageField(upload_to=renombrar_foto, blank=True, null=True)
    video = models.FileField(upload_to='videos_candidatos/', blank=True, null=True, verbose_name="Video de Presentación (Opcional)", validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi']), validar_video])
    region = models.CharField(max_length=50, choices=REGIONES_CHILE)
    experiencia = models.CharField(max_length=50, choices=NIVEL_EXPERIENCIA)
    pretension_renta = models.IntegerField(blank=True, null=True)
    disponibilidad = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    cv = models.FileField(upload_to=renombrar_archivo, blank=True, null=True)
    presentacion = models.TextField(blank=True, null=True, verbose_name="Breve presentación")
    publicado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.nombre

class Postulacion(models.Model):
    ESTADOS = [('ENV', 'Enviada'), ('VIS', 'Vista por Empresa'), ('INT', 'En Entrevista'), ('NO', 'Descartado'), ('SEL', 'Seleccionado')]
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE, related_name='postulaciones')
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='postulaciones')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=3, choices=ESTADOS, default='ENV')
    class Meta: unique_together = ('oferta', 'candidato')

class Valoracion(models.Model):
    empresa_nombre = models.CharField(max_length=200)
    estrellas = models.IntegerField(default=5)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    
    # 🔴 CORREGIDO: Agregado default para evitar error de migración
    bajada = models.TextField(default="Sin resumen disponible", blank=True)
    
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='blog/')
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    autor = models.CharField(max_length=100, default="Equipo Red Laboral")
    
    def __str__(self): return self.titulo

class Suscriptor(models.Model):
    email = models.EmailField(unique=True)
    fecha_suscripcion = models.DateTimeField(auto_now_add=True)

class AlertaEmpleo(models.Model):
    email = models.EmailField()
    palabra_clave = models.CharField(max_length=100)
    region = models.CharField(max_length=50, choices=REGIONES_CHILE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class ReporteOferta(models.Model):
    MOTIVOS = [('fraude', 'Posible Estafa'), ('discriminacion', 'Discriminación'), ('spam', 'Spam / Publicidad'), ('otro', 'Otro')]
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=50, choices=MOTIVOS)
    detalle = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=255)
    enlace = models.CharField(max_length=255, blank=True, null=True)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

class Pregunta(models.Model):
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE, related_name='preguntas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pregunta = models.TextField()
    respuesta = models.TextField(blank=True, null=True)
    fecha_pregunta = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('usuario', 'oferta')

class Servicio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicios')
    titulo = models.CharField(max_length=200, verbose_name="¿Qué servicio ofreces?")
    descripcion = models.TextField(verbose_name="Detalle del servicio")
    rubro = models.CharField(max_length=50, choices=RUBROS_CHILE)
    region = models.CharField(max_length=50, choices=REGIONES_CHILE)
    telefono = models.CharField(max_length=20, verbose_name="WhatsApp / Teléfono")
    email_contacto = models.EmailField(verbose_name="Correo de contacto")
    imagen = models.ImageField(upload_to=renombrar_archivo, blank=True, null=True)
    precio_referencial = models.CharField(max_length=100, blank=True, null=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.first_name}"