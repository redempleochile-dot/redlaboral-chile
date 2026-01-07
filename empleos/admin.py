from django.contrib import admin
# Importamos TODOS los modelos, incluyendo el nuevo 'Servicio'
from .models import (
    OfertaLaboral, Candidato, Noticia, Valoracion, Suscriptor, 
    AlertaEmpleo, Postulacion, PerfilEmpresa, ReporteOferta, 
    Notificacion, Pregunta, Favorito, Servicio
)

# --- 1. OFERTAS LABORALES ---
@admin.register(OfertaLaboral)
class OfertaAdmin(admin.ModelAdmin):
    # ✅ CORREGIDO: Eliminado 'empresa_verificada', agregado 'pagada' y 'fecha_cierre'
    list_display = ('titulo_corto', 'empresa', 'region', 'visitas', 'es_destacado', 'publicada', 'pagada')
    list_filter = ('publicada', 'pagada', 'es_destacado', 'region', 'tipo')
    search_fields = ('titulo', 'empresa', 'descripcion')
    list_editable = ('publicada', 'es_destacado', 'pagada') # Permite editar rápido desde la lista

    def titulo_corto(self, obj):
        return obj.titulo[:30] + "..." if len(obj.titulo) > 30 else obj.titulo

# --- 2. CANDIDATOS ---
@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    # ✅ CORREGIDO: Usamos campos reales del modelo
    list_display = ('nombre', 'titular', 'rubro', 'region', 'publicado') 
    list_filter = ('rubro', 'publicado', 'region', 'experiencia')
    search_fields = ('nombre', 'titular', 'email')
    list_editable = ('publicado',)

# --- 3. SERVICIOS (FREELANCERS) - NUEVO ---
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'rubro', 'region', 'publicado', 'fecha_publicacion')
    list_filter = ('publicado', 'region', 'rubro')
    search_fields = ('titulo', 'descripcion')
    list_editable = ('publicado',)

# --- 4. SUSCRIPTORES ---
@admin.register(Suscriptor)
class SuscriptorAdmin(admin.ModelAdmin):
    # ✅ CORREGIDO: 'fecha_registro' no existía, cambiamos a 'fecha_suscripcion'
    list_display = ('email', 'fecha_suscripcion')
    search_fields = ('email',)
    ordering = ('-fecha_suscripcion',)

# --- 5. PERFILES DE EMPRESA ---
@admin.register(PerfilEmpresa)
class PerfilEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'es_premium', 'es_destacada')
    list_filter = ('es_premium', 'es_destacada')
    search_fields = ('nombre', 'usuario__email', 'usuario__username')
    list_editable = ('es_premium', 'es_destacada')

# --- 6. REPORTES (MODERACIÓN) ---
@admin.register(ReporteOferta)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('oferta', 'motivo', 'fecha')
    list_filter = ('motivo',)
    readonly_fields = ('oferta', 'motivo', 'detalle', 'fecha')

# --- 7. VALORACIONES ---
@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('empresa_nombre', 'estrellas', 'aprobado', 'fecha')
    list_filter = ('aprobado', 'estrellas')
    list_editable = ('aprobado',)

# --- 8. NOTICIAS (BLOG) ---
@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido')

# --- REGISTRO DE OTROS MODELOS ---
# Modelos que no requieren configuración avanzada por ahora
admin.site.register(AlertaEmpleo)
admin.site.register(Postulacion)
admin.site.register(Notificacion)
admin.site.register(Pregunta)
admin.site.register(Favorito)