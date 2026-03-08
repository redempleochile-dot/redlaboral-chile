from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from empleos.sitemaps import OfertaSitemap

# Importación general (más segura y limpia)
from empleos import views

sitemaps = {'ofertas': OfertaSitemap}

urlpatterns = [
    # --- ADMIN DE DJANGO ---
    path('admin/', admin.site.urls),
    
    # --- PORTADA ---
    path('', views.pagina_inicio, name='home'),

    # --- AUTENTICACIÓN ---
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('cuenta/eliminar/', views.eliminar_cuenta, name='eliminar_cuenta'),
    
    # 🔥 NUEVO SEMÁFORO DE REDIRECCIÓN 🔥
    path('redireccion-inicio/', views.redireccion_post_login, name='redireccion_login'),
    
    # --- RECUPERAR CONTRASEÑA ---
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # --- OFERTAS ---
    path('oferta/<int:id>/', views.detalle_oferta, name='detalle'),
    path('oferta/editar/<uuid:token>/', views.editar_oferta, name='editar_oferta'),
    path('oferta/<int:id>/imprimir/', views.imprimir_oferta, name='imprimir'),
    path('publicar/', views.publicar_empleo, name='publicar'), 
    path('publicar_empleo/', views.publicar_empleo, name='publicar_empleo'), 
    path('practicas/', views.lista_practicas, name='lista_practicas'),
    
    # --- SERVICIOS / FREELANCE ---
    path('servicios/', views.lista_servicios, name='lista_servicios'),
    path('servicios/publicar/', views.publicar_servicio, name='publicar_servicio'),
    path('servicios/<int:id>/', views.detalle_servicio, name='detalle_servicio'),
    
    # --- FAVORITOS, Q&A, EMPRESAS ---
    path('oferta/<int:id_oferta>/favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('mis-favoritos/', views.mis_favoritos, name='mis_favoritos'),
    path('empresas/', views.lista_empresas, name='lista_empresas'),
    path('pregunta/<int:id_pregunta>/responder/', views.responder_pregunta, name='responder_pregunta'),

    # --- SEO ---
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),

    # --- GESTIÓN EMPRESA ---
    path('empresa/editar/', views.editar_empresa, name='editar_empresa'),
    path('oferta/<int:id>/reportar/', views.reportar_oferta, name='reportar_oferta'),
    path('empresa/<str:nombre_empresa>/', views.perfil_empresa, name='perfil_empresa'),
    path('mis-avisos/', views.mis_avisos, name='mis_avisos'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('postular/<int:id>/', views.postular_oferta, name='postular_oferta'),
    path('gestion-oferta/<int:id_oferta>/candidatos/', views.gestion_candidatos, name='gestion_candidatos'),
    path('gestion-oferta/<int:id_oferta>/exportar/', views.exportar_candidatos_csv, name='exportar_csv'),
    
    # --- CANDIDATOS ---
    path('candidatos/', views.lista_candidatos, name='candidatos'),
    path('candidato/<int:id>/', views.detalle_candidato, name='detalle_candidato'),
    path('candidato/<int:id>/descargar/', views.descargar_cv_pdf, name='descargar_cv'),
    path('publicar-perfil/', views.publicar_candidato, name='publicar_perfil'),
    path('publicar_candidato/', views.publicar_candidato, name='publicar_candidato'), 
    path('crear-alerta/', views.crear_alerta, name='crear_alerta'),
    
    # --- NOTIFICACIONES Y PAGOS ---
    path('notificaciones/leidas/', views.marcar_leidas, name='marcar_leidas'),
    path('planes/', views.pagina_planes, name='planes'),
    path('checkout/<str:plan>/', views.pago_simulado, name='pago_simulado'),

    # --- EXTRAS ---
    path('estadisticas/', views.pagina_estadisticas, name='estadisticas'),
    path('contacto/', views.pagina_contacto, name='contacto'),
    path('suscribir/', views.suscribir_newsletter, name='suscribir_newsletter'),
    path('blog/', views.lista_blog, name='blog'),
    path('blog/<int:id>/', views.detalle_noticia, name='detalle_noticia'),
    path('exito/', views.pagina_exito, name='pagina_exito'),
    path('mis-postulaciones/', views.mis_postulaciones, name='mis_postulaciones'),
    path('mapa/', views.mapa_empleos, name='mapa_empleos'),

    # --- LEGALES ---
    path('terminos/', views.terminos_condiciones, name='terminos'),
    path('privacidad/', views.politica_privacidad, name='privacidad'),

    path('prueba-email/', views.prueba_email, name='prueba_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)