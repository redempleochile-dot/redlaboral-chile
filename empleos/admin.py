from django.contrib import admin
from .models import (
    OfertaLaboral, Candidato, Noticia, Valoracion, Suscriptor, 
    AlertaEmpleo, Postulacion, PerfilEmpresa, ReporteOferta, 
    Notificacion, Pregunta, Favorito, Servicio
)

@admin.register(OfertaLaboral)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('titulo_corto', 'empresa', 'region', 'visitas', 'es_destacado', 'publicada', 'pagada')
    list_filter = ('publicada', 'pagada', 'es_destacado', 'region', 'tipo')
    search_fields = ('titulo', 'empresa', 'descripcion')
    list_editable = ('publicada', 'es_destacado', 'pagada')

    def titulo_corto(self, obj):
        return obj.titulo[:30] + "..." if len(obj.titulo) > 30 else obj.titulo

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'titular', 'rubro', 'region', 'publicado') 
    list_filter = ('rubro', 'publicado', 'region', 'experiencia')
    search_fields = ('nombre', 'titular', 'email')
    list_editable = ('publicado',)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'rubro', 'region', 'publicado', 'fecha_publicacion')
    list_filter = ('publicado', 'region', 'rubro')
    search_fields = ('titulo', 'descripcion')
    list_editable = ('publicado',)

@admin.register(Suscriptor)
class SuscriptorAdmin(admin.ModelAdmin):
    # ✅ CORREGIDO: Usamos el nombre correcto 'fecha_suscripcion'
    list_display = ('email', 'fecha_suscripcion')
    search_fields = ('email',)
    ordering = ('-fecha_suscripcion',)

@admin.register(PerfilEmpresa)
class PerfilEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'es_premium', 'es_destacada')
    list_filter = ('es_premium', 'es_destacada')
    search_fields = ('nombre', 'usuario__email', 'usuario__username')
    list_editable = ('es_premium', 'es_destacada')

@admin.register(ReporteOferta)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('oferta', 'motivo', 'fecha')
    list_filter = ('motivo',)
    readonly_fields = ('oferta', 'motivo', 'detalle', 'fecha')

@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('empresa_nombre', 'estrellas', 'aprobado', 'fecha')
    list_filter = ('aprobado', 'estrellas')
    list_editable = ('aprobado',)

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido')

admin.site.register(AlertaEmpleo)
admin.site.register(Postulacion)
admin.site.register(Notificacion)
admin.site.register(Pregunta)
admin.site.register(Favorito)