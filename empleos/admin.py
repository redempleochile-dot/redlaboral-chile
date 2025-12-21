from django.contrib import admin
from .models import OfertaLaboral, Candidato, Noticia, Valoracion, Suscriptor

@admin.register(OfertaLaboral)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('titulo_corto', 'empresa', 'empresa_verificada', 'visitas', 'es_destacado', 'publicada')
    list_filter = ('empresa_verificada', 'publicada', 'es_destacado', 'region')
    search_fields = ('titulo', 'empresa')
    list_editable = ('publicada', 'es_destacado', 'empresa_verificada')

    def titulo_corto(self, obj):
        return obj.titulo[:30] + "..." if len(obj.titulo) > 30 else obj.titulo

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    # CORRECCIÓN AQUÍ: cambiamos 'especialidad' por 'titular' y agregamos 'rubro'
    list_display = ('nombre', 'titular', 'rubro', 'publicado') 
    list_filter = ('rubro', 'publicado', 'region')
    search_fields = ('nombre', 'titular')
    list_editable = ('publicado',)

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_publicacion')

@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('empresa_nombre', 'estrellas', 'aprobado')
    list_editable = ('aprobado',)

@admin.register(Suscriptor)
class SuscriptorAdmin(admin.ModelAdmin):
    list_display = ('email', 'fecha_registro')