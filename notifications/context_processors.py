from .models import Notificacion


def notificaciones_context(request):
    """
    Añade al contexto global las notificaciones no leídas del usuario autenticado.
    """
    if not request.user.is_authenticated:
        return {}

    qs = Notificacion.objects.filter(
        usuario_destino=request.user,
        leida=False
    ).order_by("-fecha_envio")

    return {
        "notificaciones_no_leidas": qs,
        "total_notificaciones_no_leidas": qs.count(),
    }
