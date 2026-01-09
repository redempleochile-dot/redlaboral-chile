import uuid
import json
import random
import io
import base64
import qrcode
import time
import csv
import threading
import os
import requests 

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Avg
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse # <--- NUEVO IMPORT NECESARIO

# --- IMPORTACIONES PARA ACTIVACIÓN DE CUENTA ---
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

# IMPORTACIÓN DE MODELOS Y FORMULARIOS
from .models import (
    OfertaLaboral, Candidato, Noticia, Valoracion, Suscriptor, 
    AlertaEmpleo, Postulacion, PerfilEmpresa, ReporteOferta, Notificacion, 
    Pregunta, Favorito, Servicio,
    REGIONES_CHILE, NIVEL_EXPERIENCIA, TIPO_TRABAJO, RUBROS_CHILE
)

from .forms import (
    NuevaOfertaForm, NuevoCandidatoForm, ContactoForm, 
    ValoracionForm, SuscriptorForm, PerfilEmpresaForm, ReporteForm, 
    PreguntaForm, RegistroForm, NuevoServicioForm
)

# --- UTILIDAD: HILO PARA EMAIL (ENVÍO RÁPIDO) ---
class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                self.subject, 
                self.message, 
                settings.EMAIL_HOST_USER, 
                self.recipient_list, 
                fail_silently=False
            )
            print(f"✅ Correo enviado en segundo plano a: {self.recipient_list}")
        except Exception as e:
            print(f"⚠️ Error enviando email en segundo plano: {e}")

# =========================================================
# VISTAS GENERALES
# =========================================================

def pagina_exito(request): 
    return render(request, 'exito.html')

def pagina_inicio(request):
    all_ofertas = OfertaLaboral.objects.filter(publicada=True).order_by('-es_destacado', '-fecha_publicacion')
    
    q = request.GET.get('q')
    if q: all_ofertas = all_ofertas.filter(Q(titulo__icontains=q) | Q(empresa__icontains=q))
    
    region = request.GET.get('region')
    if region: all_ofertas = all_ofertas.filter(region=region)
    
    min_sueldo = request.GET.get('min_sueldo')
    if min_sueldo and min_sueldo.isdigit(): all_ofertas = all_ofertas.filter(sueldo__gte=int(min_sueldo))

    dias = request.GET.get('dias')
    if dias and dias.isdigit():
        fecha_limite = timezone.now() - timedelta(days=int(dias))
        all_ofertas = all_ofertas.filter(fecha_publicacion__gte=fecha_limite)

    paginator = Paginator(all_ofertas, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    empresas = PerfilEmpresa.objects.filter(es_destacada=True).exclude(logo='')
    
    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = Favorito.objects.filter(usuario=request.user).values_list('oferta_id', flat=True)

    context = {
        'ofertas_destacadas': all_ofertas.filter(es_destacado=True)[:5],
        'ofertas': page_obj, 'regiones': REGIONES_CHILE, 
        'tipos': TIPO_TRABAJO, 'niveles': NIVEL_EXPERIENCIA, 
        'form_newsletter': SuscriptorForm(), 'empresas_carrusel': empresas,
        'favoritos_ids': list(favoritos_ids)
    }
    return render(request, 'lista_ofertas.html', context)

# --- DETALLE DE OFERTA ---

def detalle_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    oferta.visitas += 1
    oferta.save(update_fields=['visitas'])
    
    similares = OfertaLaboral.objects.filter(tipo=oferta.tipo, publicada=True).exclude(id=id).order_by('-fecha_publicacion')[:3]
    
    if request.method == 'POST' and 'btn_preguntar' in request.POST:
        if not request.user.is_authenticated: 
            messages.warning(request, "Inicia sesión para preguntar.")
            return redirect('login')
        form_pregunta = PreguntaForm(request.POST)
        if form_pregunta.is_valid():
            preg = form_pregunta.save(commit=False)
            preg.oferta = oferta
            preg.usuario = request.user
            preg.save()
            if oferta.usuario: 
                Notificacion.objects.create(usuario=oferta.usuario, mensaje=f"❓ Nueva pregunta en {oferta.titulo}", enlace=f"/oferta/{oferta.id}/")
            messages.success(request, "Pregunta enviada.")
            return redirect('detalle', id=id)
    else: 
        form_pregunta = PreguntaForm()

    match_percent = None
    match_details = []
    if request.user.is_authenticated:
        try:
            candidato = request.user.candidato
            score = 0
            if oferta.region == candidato.region: score += 1; match_details.append({'icon':'✅', 'text':'Misma Región'})
            else: match_details.append({'icon':'❌', 'text':'Diferente Región'})
            
            if oferta.sueldo and candidato.pretension_renta:
                if oferta.sueldo >= candidato.pretension_renta * 0.9: score += 1; match_details.append({'icon':'✅', 'text':'Sueldo Acorde'})
                else: match_details.append({'icon':'⚠️', 'text':'Sueldo bajo tu pretensión'})
            else: score += 0.5; match_details.append({'icon':'⚖️', 'text':'Sueldo a negociar'})
            
            if candidato.titular and oferta.titulo and candidato.titular.lower() in oferta.titulo.lower(): score += 1; match_details.append({'icon':'✅', 'text':'Perfil Técnico Compatible'})
            else: score += 0.5; match_details.append({'icon':'🔍', 'text':'Revisar requisitos'})
            
            match_percent = int((score / 3) * 100)
        except: pass

    return render(request, 'detalle_oferta.html', {
        'oferta': oferta, 'similares': similares, 'match_percent': match_percent, 
        'match_details': match_details, 'form_pregunta': form_pregunta
    })

# =========================================================
# GESTIÓN DE EMPRESAS Y OFERTAS
# =========================================================

def publicar_empleo(request):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Para publicar ofertas, inicia sesión o regístrate como empresa.")
        return redirect('login')

    if request.method == 'POST':
        form = NuevaOfertaForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.usuario = request.user
            oferta.pagada = True       
            oferta.publicada = True    
            oferta.save()
            
            # Sistema de Alertas Automáticas
            try:
                palabras = oferta.titulo.split() if oferta.titulo else []
                query = Q(region=oferta.region) & (Q(palabra_clave__icontains=oferta.titulo) | Q(palabra_clave__in=palabras))
                alertas_coincidentes = AlertaEmpleo.objects.filter(query)
                destinatarios = list(set([alerta.email for alerta in alertas_coincidentes]))
                if destinatarios: 
                    mensaje = f"Nueva oferta: {oferta.titulo}. Postula aquí: https://www.buscapegachile.cl/oferta/{oferta.id}/"
                    EmailThread(f"🔔 Alerta: {oferta.titulo}", mensaje, destinatarios).start()
            except Exception as e: 
                print(f"Error alertas: {e}")

            messages.success(request, "¡Oferta publicada exitosamente!")
            return redirect('pagina_exito') 
    else: 
        form = NuevaOfertaForm()
    return render(request, 'publicar_empleo.html', {'form': form})

@login_required
def mis_avisos(request): 
    mis_ofertas = OfertaLaboral.objects.filter(usuario=request.user).order_by('-fecha_publicacion')
    return render(request, 'mis_avisos.html', {'ofertas': mis_ofertas})

@login_required
def editar_empresa(request):
    perfil, created = PerfilEmpresa.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        form = PerfilEmpresaForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid(): 
            form.save()
            messages.success(request, "Perfil de empresa actualizado.")
            return redirect('mis_avisos')
    else: 
        form = PerfilEmpresaForm(instance=perfil)
    return render(request, 'editar_empresa.html', {'form': form})

@login_required
def editar_oferta(request, token):
    oferta = get_object_or_404(OfertaLaboral, token=token)
    if request.method == 'POST':
        if 'borrar' in request.POST: 
            oferta.delete()
            messages.success(request, 'Oferta eliminada.')
            return redirect('/')
        form = NuevaOfertaForm(request.POST, request.FILES, instance=oferta)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'Oferta actualizada.')
            return redirect('detalle', id=oferta.id)
    else: 
        form = NuevaOfertaForm(instance=oferta)
    return render(request, 'editar_oferta.html', {'form': form, 'oferta': oferta})

def lista_empresas(request):
    empresas = PerfilEmpresa.objects.exclude(nombre__isnull=True).exclude(logo='')
    q = request.GET.get('q')
    if q: empresas = empresas.filter(nombre__icontains=q)
    return render(request, 'lista_empresas.html', {'empresas': empresas})

def perfil_empresa(request, nombre_empresa):
    perfil = PerfilEmpresa.objects.filter(nombre__iexact=nombre_empresa).first()
    ofertas = OfertaLaboral.objects.filter(empresa__icontains=nombre_empresa, publicada=True).order_by('-fecha_publicacion')
    
    if request.method == 'POST':
        form = ValoracionForm(request.POST)
        if form.is_valid(): 
            val = form.save(commit=False)
            val.empresa_nombre = nombre_empresa
            val.save()
            messages.success(request, "Valoración enviada.")
            return redirect('perfil_empresa', nombre_empresa=nombre_empresa)
    else: 
        form = ValoracionForm()
    
    val = Valoracion.objects.filter(empresa_nombre__icontains=nombre_empresa, aprobado=True).order_by('-fecha')
    avg = val.aggregate(Avg('estrellas'))['estrellas__avg']
    return render(request, 'perfil_empresa.html', {'nombre_empresa': nombre_empresa, 'perfil': perfil, 'ofertas': ofertas, 'valoraciones': val, 'promedio': round(avg, 1) if avg else None, 'form': form})

# =========================================================
# GESTIÓN DE CANDIDATOS
# =========================================================

def publicar_candidato(request):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Para publicar tu CV, inicia sesión o regístrate.")
        return redirect('login')

    try: candidato = request.user.candidato
    except: candidato = None

    if request.method == 'POST':
        form = NuevoCandidatoForm(request.POST, request.FILES, instance=candidato)
        if form.is_valid(): 
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            messages.success(request, "CV Actualizado correctamente.")
            return redirect('pagina_exito')
    else: 
        form = NuevoCandidatoForm(instance=candidato)
    return render(request, 'publicar_candidato.html', {'form': form})

@login_required
def postular_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    try: candidato = request.user.candidato
    except: 
        messages.error(request, "Crea tu Perfil Profesional antes de postular.")
        return redirect('publicar_candidato')
    
    if Postulacion.objects.filter(oferta=oferta, candidato=candidato).exists(): 
        messages.warning(request, "Ya has enviado tu perfil a esta oferta.")
        return redirect('detalle', id=id)
    
    Postulacion.objects.create(oferta=oferta, candidato=candidato)
    if oferta.usuario: 
        Notificacion.objects.create(usuario=oferta.usuario, mensaje=f"📄 Nuevo candidato: {candidato.nombre} postuló a {oferta.titulo}", enlace=f"/gestion-oferta/{oferta.id}/candidatos/")
    messages.success(request, "¡Postulación enviada con éxito!")
    return redirect('detalle', id=id)

@login_required
def gestion_candidatos(request, id_oferta):
    oferta = get_object_or_404(OfertaLaboral, id=id_oferta, usuario=request.user)
    postulaciones = oferta.postulaciones.all().order_by('-fecha')
    if request.method == 'POST':
        post_id = request.POST.get('postulacion_id')
        nuevo_estado = request.POST.get('nuevo_estado')
        postulacion = get_object_or_404(Postulacion, id=post_id)
        postulacion.estado = nuevo_estado
        postulacion.save()
        
        mensaje_candidato = ""
        if nuevo_estado == 'VIS': mensaje_candidato = f"👀 Tu postulación a {oferta.titulo} fue vista."
        elif nuevo_estado == 'INT': mensaje_candidato = f"🎉 ¡Felicidades! Pasaste a entrevista en {oferta.titulo}."
        elif nuevo_estado == 'NO': mensaje_candidato = f"❌ Tu proceso en {oferta.titulo} ha finalizado."
        
        if mensaje_candidato and postulacion.candidato.usuario: 
            Notificacion.objects.create(usuario=postulacion.candidato.usuario, mensaje=mensaje_candidato, enlace=f"/oferta/{oferta.id}/")
        
        messages.success(request, "Estado actualizado.")
        return redirect('gestion_candidatos', id_oferta=id_oferta)
    return render(request, 'gestion_candidatos.html', {'oferta': oferta, 'postulaciones': postulaciones})

@login_required
def exportar_candidatos_csv(request, id_oferta):
    oferta = get_object_or_404(OfertaLaboral, id=id_oferta, usuario=request.user)
    if not hasattr(request.user, 'perfil_empresa'):
        messages.error(request, "Acción exclusiva para empresas registradas.")
        return redirect('home')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Postulantes_{oferta.id}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Email', 'Teléfono', 'Titulo', 'Estado', 'Fecha'])
    for post in oferta.postulaciones.all(): 
        writer.writerow([post.candidato.nombre, post.candidato.email, post.candidato.telefono, post.candidato.titular, post.get_estado_display(), post.fecha.strftime("%d-%m-%Y")])
    return response

def lista_candidatos(request):
    candidatos = Candidato.objects.filter(publicado=True).order_by('-fecha_creacion')
    rubro = request.GET.get('rubro')
    region = request.GET.get('region')
    if rubro: candidatos = candidatos.filter(rubro=rubro)
    if region: candidatos = candidatos.filter(region=region)
    return render(request, 'lista_candidatos.html', {'candidatos': candidatos, 'regiones': REGIONES_CHILE, 'rubros': RUBROS_CHILE})

def detalle_candidato(request, id):
    candidato = get_object_or_404(Candidato, id=id)
    if not candidato.publicado: 
        messages.error(request, "Perfil no disponible.")
        return redirect('candidatos')
    
    puede_ver_contacto = False
    if request.user.is_authenticated:
        if hasattr(request.user, 'candidato') and request.user.candidato.id == candidato.id: 
            puede_ver_contacto = True
        elif hasattr(request.user, 'perfil_empresa'): 
            puede_ver_contacto = True
        elif request.user.is_staff: 
            puede_ver_contacto = True

    return render(request, 'detalle_candidato.html', {'candidato': candidato, 'puede_ver_contacto': puede_ver_contacto})

def descargar_cv_pdf(request, id):
    candidato = get_object_or_404(Candidato, id=id)
    template_path = 'pdf/cv_template.html'
    context = {'candidato': candidato}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CV_{candidato.nombre}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err: return HttpResponse('Error al generar PDF')
    return response

@login_required
def mis_postulaciones(request):
    try: candidato = request.user.candidato
    except: 
        messages.warning(request, "Primero crea tu Perfil de Talento.")
        return redirect('publicar_candidato')
    postulaciones = Postulacion.objects.filter(candidato=candidato).order_by('-fecha')
    return render(request, 'mis_postulaciones.html', {'postulaciones': postulaciones, 'candidato': candidato})

@login_required
def toggle_favorito(request, id_oferta):
    oferta = get_object_or_404(OfertaLaboral, id=id_oferta)
    favorito, created = Favorito.objects.get_or_create(usuario=request.user, oferta=oferta)
    if not created: 
        favorito.delete()
        messages.info(request, "Eliminado de favoritos.")
    else: 
        messages.success(request, "Guardado en favoritos ❤️")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def mis_favoritos(request):
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('oferta').order_by('-fecha')
    return render(request, 'mis_favoritos.html', {'favoritos': favoritos})

@login_required
def responder_pregunta(request, id_pregunta):
    pregunta = get_object_or_404(Pregunta, id=id_pregunta)
    if request.user == pregunta.oferta.usuario:
        respuesta_texto = request.POST.get('respuesta')
        if respuesta_texto:
            pregunta.respuesta = respuesta_texto
            pregunta.fecha_respuesta = timezone.now()
            pregunta.save()
            messages.success(request, "Respuesta publicada.")
            Notificacion.objects.create(usuario=pregunta.usuario, mensaje=f"💬 Respondieron tu pregunta en {pregunta.oferta.titulo}", enlace=f"/oferta/{pregunta.oferta.id}/")
    return redirect('detalle', id=pregunta.oferta.id)

@login_required
def marcar_leidas(request): 
    Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# =========================================================
# USUARIOS Y AUTENTICACIÓN (REGISTRO Y ACTIVACIÓN)
# =========================================================

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        
        # --- VERIFICACIÓN CLOUDFLARE ---
        turnstile_token = request.POST.get('cf-turnstile-response')
        SECRET_KEY_CLOUDFLARE = "0x4AAAAAACKuVgshdJoeBm5ANHQWv_SkzeQ" 
        
        if not turnstile_token:
             messages.error(request, "⚠️ Por seguridad, completa el captcha 'No soy un robot'.")
             return render(request, 'registration/registro.html', {'form': form})

        try:
            verificacion = requests.post(
                'https://challenges.cloudflare.com/turnstile/v0/siteverify',
                data={
                    'secret': SECRET_KEY_CLOUDFLARE,
                    'response': turnstile_token,
                    'remoteip': request.META.get('REMOTE_ADDR')
                }
            ).json()

            if not verificacion.get('success'):
                messages.error(request, "🤖 Verificación fallida. Intenta de nuevo.")
                return render(request, 'registration/registro.html', {'form': form})
                
        except Exception as e:
            print(f"Error Cloudflare: {e}")
            pass

        # --- GUARDADO DEL USUARIO ---
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            domain = "www.buscapegachile.cl"
            link = f"https://{domain}/activar/{uid}/{token}/"
            
            asunto = "🚀 Activa tu cuenta en Busca Pega Chile"
            mensaje = f"""
            Hola {user.first_name},
            
            Haz clic en el siguiente enlace para verificar tu correo y activar tu cuenta:
            {link}
            
            Si no fuiste tú, ignora este correo.
            """
            
            EmailThread(asunto, mensaje, [user.email]).start()
            
            # 🔥 CORRECCIÓN INFALIBLE: Redirigir con señal en la URL 🔥
            # Esto evita que el mensaje se pierda por problemas de cookies/SSL
            url_login = reverse('login')
            return redirect(f'{url_login}?registro_exitoso=True')

        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = RegistroForm()
        
    return render(request, 'registration/registro.html', {'form': form})

def activar_cuenta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "🎉 ¡Cuenta verificada exitosamente! Bienvenido.")
        return redirect('home')
    else:
        messages.error(request, "El enlace de activación es inválido o ya expiró.")
        return redirect('home')

def logout_usuario(request): 
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('home')

@login_required
def eliminar_cuenta(request):
    if request.method == 'POST': 
        request.user.delete()
        messages.success(request, "Tu cuenta ha sido eliminada permanentemente.")
        return redirect('home')
    return render(request, 'registration/eliminar_cuenta.html')

# --- SECCIÓN DE SERVICIOS / FREELANCE ---

@login_required
def publicar_servicio(request):
    if request.method == 'POST':
        form = NuevoServicioForm(request.POST, request.FILES)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.usuario = request.user
            servicio.publicado = True
            servicio.save()
            messages.success(request, "¡Tu servicio ha sido publicado!")
            return redirect('lista_servicios')
    else:
        initial_data = {'email_contacto': request.user.email}
        if hasattr(request.user, 'candidato'):
            initial_data['telefono'] = request.user.candidato.telefono
        form = NuevoServicioForm(initial=initial_data)
        
    return render(request, 'servicios/publicar_servicio.html', {'form': form})

def lista_servicios(request):
    servicios = Servicio.objects.filter(publicado=True).order_by('-fecha_publicacion')
    
    rubro = request.GET.get('rubro')
    region = request.GET.get('region')
    q = request.GET.get('q')
    
    if rubro: servicios = servicios.filter(rubro=rubro)
    if region: servicios = servicios.filter(region=region)
    if q: servicios = servicios.filter(titulo__icontains=q)
    
    return render(request, 'servicios/lista_servicios.html', {
        'servicios': servicios,
        'rubros': RUBROS_CHILE,
        'regiones': REGIONES_CHILE
    })

def detalle_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    return render(request, 'servicios/detalle_servicio.html', {'servicio': servicio})

# --- ADMIN PANEL ---

@staff_member_required
def panel_admin(request):
    total_ofertas = OfertaLaboral.objects.count()
    total_candidatos = Candidato.objects.count()
    total_usuarios = User.objects.count()
    datos_region = OfertaLaboral.objects.values('region').annotate(total=Count('region')).order_by('-total')
    labels_reg = [dict(REGIONES_CHILE).get(x['region'], x['region']) for x in datos_region]
    data_reg = [x['total'] for x in datos_region]
    publicadas = OfertaLaboral.objects.filter(publicada=True).count()
    pendientes = OfertaLaboral.objects.filter(publicada=False).count()
    context = {'kpi_ofertas': total_ofertas, 'kpi_candidatos': total_candidatos, 'kpi_usuarios': total_usuarios, 'labels_reg': json.dumps(labels_reg), 'data_reg': json.dumps(data_reg), 'data_pie': json.dumps([publicadas, pendientes])}
    return render(request, 'panel_admin.html', context)

# --- EXTRAS (MAPA, QR, PAGOS, ETC) ---

def crear_alerta(request):
    if request.method == 'POST': 
        email = request.POST.get('email')
        clave = request.POST.get('palabra_clave')
        region = request.POST.get('region')
        AlertaEmpleo.objects.create(email=email, palabra_clave=clave, region=region)
        messages.success(request, f"¡Alerta creada!")
    return redirect('home')

def robots_txt(request): return render(request, 'robots.txt', content_type="text/plain")
def pagina_planes(request): return render(request, 'planes.html')

@login_required
def pago_simulado(request, plan):
    precio = "0"; nombre_plan = ""
    if plan == 'pro': precio = "29.990"; nombre_plan = "Plan Reclutador PRO"
    elif plan == 'corp': precio = "59.990"; nombre_plan = "Plan Corporativo"
    if request.method == 'POST':
        time.sleep(2)
        try: 
            perfil = request.user.perfil_empresa
            perfil.es_premium = True
            perfil.save()
            messages.success(request, f"¡Pago exitoso! Bienvenido al {nombre_plan}.")
            return redirect('mis_avisos')
        except: 
            messages.error(request, "Error: Solo empresas pueden comprar.")
            return redirect('home')
    return render(request, 'pago_simulado.html', {'precio': precio, 'nombre_plan': nombre_plan})

def suscribir_newsletter(request):
    if request.method == 'POST': 
        form = SuscriptorForm(request.POST)
        if form.is_valid(): form.save()
        messages.success(request, 'Gracias por suscribirte.')
    return redirect('home')

def pagina_estadisticas(request):
    datos = OfertaLaboral.objects.filter(publicada=True).values('region').annotate(total=Count('region')); labels, data = [], []
    dicc = dict(REGIONES_CHILE)
    for item in datos: labels.append(dicc.get(item['region'], item['region'])); data.append(item['total'])
    return render(request, 'estadisticas.html', {'labels_grafico': json.dumps(labels), 'data_grafico': json.dumps(data)})

def pagina_contacto(request):
    if request.method == 'POST': pass 
    return render(request, 'contacto.html', {'form': ContactoForm()})

def lista_blog(request): return render(request, 'blog.html', {'noticias': Noticia.objects.all().order_by('-fecha_publicacion')})
def detalle_noticia(request, id): return render(request, 'detalle_noticia.html', {'noticia': get_object_or_404(Noticia, id=id)})
def terminos_condiciones(request): return render(request, 'legales/terminos.html')
def politica_privacidad(request): return render(request, 'legales/privacidad.html')

def lista_practicas(request):
    practicas = OfertaLaboral.objects.filter(tipo='PRA', publicada=True).order_by('-fecha_publicacion')
    if request.GET.get('region'): practicas = practicas.filter(region=request.GET.get('region'))
    return render(request, 'lista_practicas.html', {'practicas': practicas, 'regiones': REGIONES_CHILE})

def imprimir_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    url_oferta = request.build_absolute_uri(f"/oferta/{oferta.id}/")
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url_oferta)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return render(request, 'imprimir.html', {'oferta': oferta, 'qr_b64': img_str})

def reportar_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid(): 
            reporte = form.save(commit=False)
            reporte.oferta = oferta
            reporte.save()
            messages.warning(request, "Reporte recibido. Lo revisaremos pronto.")
    return redirect('detalle', id=id)

def mapa_empleos(request):
    ofertas = OfertaLaboral.objects.filter(publicada=True)
    marcadores = []
    COORDENADAS_REGIONES = {'AP': [-18.4783, -70.3126], 'TA': [-20.2133, -70.1503], 'AN': [-23.6509, -70.3975], 'AT': [-27.3668, -70.3323], 'CO': [-29.9533, -71.3436], 'VA': [-33.0472, -71.6127], 'RM': [-33.4489, -70.6693], 'BI': [-36.8201, -73.0444], 'AR': [-38.7359, -72.5904], 'LS': [-41.4689, -72.9411], 'AI': [-45.5712, -72.0685], 'MA': [-53.1638, -70.9171], 'NB': [-36.6063, -72.1023], 'LR': [-39.8142, -73.2459]}
    
    for oferta in ofertas:
        coords = COORDENADAS_REGIONES.get(oferta.region)
        if coords: 
            marcadores.append({
                'lat': coords[0] + random.uniform(-0.02, 0.02), 
                'lng': coords[1] + random.uniform(-0.02, 0.02), 
                'titulo': oferta.titulo, 
                'empresa': oferta.empresa, 
                'url': f"/oferta/{oferta.id}/", 
                'tipo': oferta.get_tipo_display()
            })
    return render(request, 'mapa.html', {'marcadores_json': json.dumps(marcadores)})

def prueba_email(request):
    try:
        send_mail(
            'Prueba de Fuego 🔥',
            'Si lees esto, ¡la configuración de correo funciona perfectamente!',
            settings.EMAIL_HOST_USER,
            ['millapeld@gmail.com'], 
            fail_silently=False,
        )
        return HttpResponse("✅ ¡ÉXITO! El correo fue enviado.")
    except Exception as e:
        return HttpResponse(f"❌ ERROR DETALLADO: {e}")