from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from empleos.sitemaps import OfertaSitemap
from django.contrib.auth import views as auth_views

from empleos.views import (
    pagina_inicio, detalle_oferta, publicar_empleo, 
    lista_candidatos, publicar_candidato, pagina_exito, 
    pagina_planes, pagina_estadisticas, pagina_contacto,
    perfil_empresa, suscribir_newsletter,
    lista_blog, detalle_noticia, imprimir_oferta,
    editar_oferta, mis_postulaciones,
    mapa_empleos, registro_usuario, logout_usuario,
    eliminar_cuenta, terminos_condiciones, politica_privacidad,
    detalle_candidato, descargar_cv_pdf,
    mis_avisos, panel_admin, crear_alerta,
    lista_practicas, postular_oferta, gestion_candidatos,
    editar_empresa, reportar_oferta, marcar_leidas,
    pago_simulado, robots_txt, exportar_candidatos_csv,
    lista_empresas, responder_pregunta, toggle_favorito, mis_favoritos # <--- ¡TODOS INCLUIDOS!
)

sitemaps = {'ofertas': OfertaSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pagina_inicio, name='home'),
    
    # OFERTAS
    path('oferta/<int:id>/', detalle_oferta, name='detalle'),
    path('oferta/editar/<uuid:token>/', editar_oferta, name='editar_oferta'),
    path('oferta/<int:id>/imprimir/', imprimir_oferta, name='imprimir'),
    path('publicar/', publicar_empleo, name='publicar'),
    path('practicas/', lista_practicas, name='lista_practicas'),
    
    # FAVORITOS, Q&A, EMPRESAS
    path('oferta/<int:id_oferta>/favorito/', toggle_favorito, name='toggle_favorito'),
    path('mis-favoritos/', mis_favoritos, name='mis_favoritos'),
    path('empresas/', lista_empresas, name='lista_empresas'),
    path('pregunta/<int:id_pregunta>/responder/', responder_pregunta, name='responder_pregunta'),

    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),

    # GESTIÓN EMPRESA
    path('empresa/editar/', editar_empresa, name='editar_empresa'),
    path('oferta/<int:id>/reportar/', reportar_oferta, name='reportar_oferta'),
    path('empresa/<str:nombre_empresa>/', perfil_empresa, name='perfil_empresa'),
    path('mis-avisos/', mis_avisos, name='mis_avisos'),
    path('panel-admin/', panel_admin, name='panel_admin'),
    path('postular/<int:id>/', postular_oferta, name='postular_oferta'),
    path('gestion-oferta/<int:id_oferta>/candidatos/', gestion_candidatos, name='gestion_candidatos'),
    path('gestion-oferta/<int:id_oferta>/exportar/', exportar_candidatos_csv, name='exportar_csv'),
    
    # CANDIDATOS
    path('candidatos/', lista_candidatos, name='candidatos'),
    path('candidato/<int:id>/', detalle_candidato, name='detalle_candidato'),
    path('candidato/<int:id>/descargar/', descargar_cv_pdf, name='descargar_cv'),
    path('publicar-perfil/', publicar_candidato, name='publicar_perfil'),
    path('crear-alerta/', crear_alerta, name='crear_alerta'),
    
    # NOTIFICACIONES Y PAGOS
    path('notificaciones/leidas/', marcar_leidas, name='marcar_leidas'),
    path('planes/', pagina_planes, name='planes'),
    path('checkout/<str:plan>/', pago_simulado, name='pago_simulado'),

    # EXTRAS
    path('estadisticas/', pagina_estadisticas, name='estadisticas'),
    path('contacto/', pagina_contacto, name='contacto'),
    path('suscribir/', suscribir_newsletter, name='suscribir_newsletter'),
    path('blog/', lista_blog, name='blog'),
    path('blog/<int:id>/', detalle_noticia, name='detalle_noticia'),
    path('exito/', pagina_exito, name='pagina_exito'),
    path('mis-postulaciones/', mis_postulaciones, name='mis_postulaciones'),
    path('mapa/', mapa_empleos, name='mapa_empleos'),
    
    # USUARIOS
    path('registro/', registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_usuario, name='logout'),
    path('cuenta/eliminar/', eliminar_cuenta, name='eliminar_cuenta'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # LEGALES
    path('terminos/', terminos_condiciones, name='terminos'),
    path('privacidad/', politica_privacidad, name='privacidad'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)