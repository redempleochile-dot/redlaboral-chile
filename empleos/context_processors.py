from .models import Notificacion

def notificaciones_globales(request):
    if request.user.is_authenticated:
        # Traemos las últimas 5 notificaciones no leídas
        notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False).order_by('-fecha')[:5]
        return {'mis_notificaciones': notificaciones}
    return {}