import uuid
import os
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# --- FUNCIONES AUXILIARES ---
def renombrar_archivo(instance, filename):
    ext = filename.split('.')[-1]; filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('cvs_candidatos/', filename)
def renombrar_logo(instance, filename):
    ext = filename.split('.')[-1]; filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('logos_empresas/', filename)
def renombrar_foto(instance, filename):
    ext = filename.split('.')[-1]; filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('fotos_perfil/', filename)

def validar_video(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024: # 10MB
        raise ValidationError("El video no puede pesar más de 10MB.")

# --- CONSTANTES ---
REGIONES_CHILE = [('AP', 'Arica y Parinacota'), ('TA', 'Tarapacá'), ('AN', 'Antofagasta'), ('AT', 'Atacama'), ('CO', 'Coquimbo'), ('VA', 'Valparaíso'), ('RM', 'Metropolitana de Santiago'), ('BI', 'Biobío'), ('AR', 'Araucanía'), ('LS', 'Los Lagos'), ('AI', 'Aysén'), ('MA', 'Magallanes'), ('NB', 'Ñuble'), ('LR', 'Los Ríos')]
NIVEL_EXPERIENCIA = [('JR', 'Junior / Recién Egresado'), ('SSR', 'Semi Senior (2-5 años)'), ('SR', 'Senior (+5 años)')]
RUBROS_CHILE = [('ADM', 'Administración y Oficina 📁'), ('AGR', 'Agroindustria / Forestal 🌲'), ('CONS', 'Construcción e Inmobiliaria 🏗️'), ('EDU', 'Educación y Capacitación 🎓'), ('GAS', 'Gastronomía y Turismo 🍽️'), ('LOG', 'Logística, Bodega y Transporte 🚚'), ('MIN', 'Minería e Industria ⛏️'), ('SAL', 'Salud y Medicina 🏥'), ('TEC', 'Tecnología e Informática 💻'), ('VTA', 'Ventas y Retail 🛒'), ('OFI', 'Oficios Varios 🔧'), ('OTR', 'Otros Servicios')]
TIPO_TRABAJO = [('PRO', 'Profesional'), ('OFI', 'Técnico / Oficio'), ('PRA', 'Práctica Profesional 🎓')]
MODALIDAD_TRABAJO = [('PRE', 'Presencial 🏢'), ('HIB', 'Híbrido 🌗'), ('REM', '100% Remoto 🏠')]

# --- MODELOS ---
class PerfilEmpresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_empresa')
    nombre = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to=renombrar_logo, null=True, blank=True)
    banner = models.ImageField(upload_to='banners_empresas/', null=True, blank=True)
    sitio_web = models.URLField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    es_premium = models.BooleanField(default=False)
    es_destacada = models.BooleanField(default=False)
    def __str__(self): return self.nombre or "Empresa sin nombre"

class OfertaLaboral(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=2, choices=REGIONES_CHILE, default='RM', blank=True, null=True)
    experiencia = models.CharField(max_length=3, choices=NIVEL_EXPERIENCIA, default='JR', blank=True, null=True)
    tipo = models.CharField(max_length=3, choices=TIPO_TRABAJO, default='OFI', blank=True, null=True)
    modalidad = models.CharField(max_length=3, choices=MODALIDAD_TRABAJO, default='PRE', blank=True, null=True)
    sueldo = models.PositiveIntegerField(null=True, blank=True)
    duracion = models.CharField(max_length=100, blank=True, null=True)
    fecha_cierre = models.DateField(default=timezone.now, blank=True, null=True)
    
    telefono = models.CharField(max_length=20, blank=True, null=True)
    wsp_activo = models.BooleanField(default=False, verbose_name="¿Contactar por WhatsApp?") # <--- NUEVO
    email_contacto = models.EmailField(blank=True, null=True)
    
    etiquetas = models.CharField(max_length=200, blank=True, null=True)
    imagen = models.ImageField(upload_to=renombrar_logo, null=True, blank=True)
    visitas = models.PositiveIntegerField(default=0)
    es_destacado = models.BooleanField(default=False)
    publicada = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    empresa_verificada = models.BooleanField(default=False)

    def __str__(self): return f"{self.titulo or 'Sin título'} - {self.empresa or 'Confidencial'}"
    def es_nueva(self): return self.fecha_publicacion >= timezone.now() - timedelta(days=3)
    def get_absolute_url(self): return reverse('detalle', args=[str(self.id)])
    def dias_para_cierre(self): 
        if self.fecha_cierre: return (self.fecha_cierre - timezone.now().date()).days
        return 0
    def telefono_limpio(self): # <--- NUEVO
        if self.telefono: return ''.join(filter(str.isdigit, self.telefono))
        return ""
    def termometro_salarial(self):
        if not self.sueldo: return None
        if self.sueldo < 500000: return {'width': '25%', 'color': 'bg-danger', 'msg': 'Inicial'}
        if self.sueldo < 900000: return {'width': '50%', 'color': 'bg-warning', 'msg': 'Mercado'}
        if self.sueldo < 1500000: return {'width': '75%', 'color': 'bg-info', 'msg': 'Competitivo'}
        return {'width': '100%', 'color': 'bg-success', 'msg': 'Alto Nivel'}

class Candidato(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='candidato')
    nombre = models.CharField(max_length=100, blank=True, null=True)
    titular = models.CharField(max_length=100, blank=True, null=True)
    rubro = models.CharField(max_length=4, choices=RUBROS_CHILE, default='OTR', blank=True, null=True)
    foto = models.ImageField(upload_to=renombrar_foto, null=True, blank=True)
    
    # NUEVO: VIDEO
    video = models.FileField(upload_to='videos_candidatos/', null=True, blank=True, validators=[FileExtensionValidator(['mp4', 'mov', 'avi']), validar_video])

    pretension_renta = models.PositiveIntegerField(null=True, blank=True)
    disponibilidad = models.CharField(max_length=50, default="Inmediata", blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    region = models.CharField(max_length=2, choices=REGIONES_CHILE, default='RM', blank=True, null=True)
    experiencia = models.CharField(max_length=3, choices=NIVEL_EXPERIENCIA, default='JR', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    presentacion = models.TextField(blank=True, null=True)
    cv = models.FileField(upload_to=renombrar_archivo, null=True, blank=True, validators=[FileExtensionValidator(['pdf'])])
    publicado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.nombre or 'Anónimo'} - {self.titular or 'Sin cargo'}"

class Postulacion(models.Model):
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE, related_name='postulaciones')
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=3, choices=[('ENV', 'Enviada 📩'), ('VIS', 'Visto 👀'), ('INT', 'Entrevista 🤝'), ('NO', 'Descartado ❌')], default='ENV')
    class Meta: unique_together = ('oferta', 'candidato')

class Pregunta(models.Model):
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE, related_name='preguntas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pregunta = models.TextField(); respuesta = models.TextField(blank=True, null=True); fecha_pregunta = models.DateTimeField(auto_now_add=True); fecha_respuesta = models.DateTimeField(blank=True, null=True)

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE, related_name='favoritos_usuarios')
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('usuario', 'oferta')

class Notificacion(models.Model): usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones'); mensaje = models.CharField(max_length=255); enlace = models.CharField(max_length=200, blank=True, null=True); leida = models.BooleanField(default=False); fecha = models.DateTimeField(auto_now_add=True)
class AlertaEmpleo(models.Model): email = models.EmailField(); palabra_clave = models.CharField(max_length=100); region = models.CharField(max_length=2, choices=REGIONES_CHILE); fecha_creacion = models.DateTimeField(auto_now_add=True)
class Noticia(models.Model): titulo = models.CharField(max_length=200); imagen = models.ImageField(upload_to='noticias', null=True, blank=True); contenido = models.TextField(); fecha_publicacion = models.DateTimeField(auto_now_add=True)
class Valoracion(models.Model): empresa_nombre = models.CharField(max_length=100); estrellas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]); comentario = models.TextField(); fecha = models.DateTimeField(auto_now_add=True); aprobado = models.BooleanField(default=True)
class Suscriptor(models.Model): email = models.EmailField(unique=True); fecha_registro = models.DateTimeField(auto_now_add=True)
class ReporteOferta(models.Model): oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE); motivo = models.CharField(max_length=3); detalle = models.TextField(blank=True); fecha = models.DateTimeField(auto_now_add=True); resuelto = models.BooleanField(default=False)
# --- MODELO DE SERVICIOS / FREELANCE ---
class Servicio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicios')
    titulo = models.CharField(max_length=200, verbose_name="¿Qué servicio ofreces?") # Ej: Desarrollo Web, Gasfitería
    descripcion = models.TextField(verbose_name="Detalle del servicio")
    rubro = models.CharField(max_length=50, choices=RUBROS_CHILE)
    region = models.CharField(max_length=50, choices=REGIONES_CHILE)
    
    # Datos de contacto específicos para este servicio
    telefono = models.CharField(max_length=20, verbose_name="WhatsApp / Teléfono")
    email_contacto = models.EmailField(verbose_name="Correo de contacto")
    
    # Imagen del trabajo (Portafolio o foto referencial)
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    
    precio_referencial = models.CharField(max_length=100, blank=True, null=True, placeholder="Ej: Desde $20.000, A convenir...")
    
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    publicado = models.BooleanField(default=True) # Se publica directo (Modo Gratis)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.first_name}"