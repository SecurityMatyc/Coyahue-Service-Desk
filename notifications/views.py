from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Notificacion


@login_required
def notificaciones_listar(request):
    notificaciones = (
        Notificacion.objects
        .filter(usuario_destino=request.user)
        .order_by("-fecha_envio")
    )
    return render(request, "notificaciones/listar.html", {
        "notificaciones": notificaciones,
    })


@login_required
def notificacion_marcar_leida(request, notif_id):
    notif = get_object_or_404(
        Notificacion,
        id=notif_id,
        usuario_destino=request.user,
    )
    notif.leida = True
    notif.save()
    return redirect("notificaciones_listar")


@login_required
def marcar_todas_leidas(request):
    """Marca todas las notificaciones del usuario como leídas"""
    cantidad = Notificacion.objects.filter(
        usuario_destino=request.user,
        leida=False
    ).update(leida=True)
    
    if cantidad > 0:
        messages.success(request, f"✓ {cantidad} notificación(es) marcada(s) como leída(s)")
    else:
        messages.info(request, "No hay notificaciones pendientes")
    
    return redirect("notificaciones_listar")


@login_required
def eliminar_todas_notificaciones(request):
    """Elimina todas las notificaciones del usuario"""
    if request.method == "POST":
        cantidad = Notificacion.objects.filter(usuario_destino=request.user).count()
        Notificacion.objects.filter(usuario_destino=request.user).delete()
        messages.success(request, f"🗑️ {cantidad} notificación(es) eliminada(s)")
        return redirect("notificaciones_listar")
    
    # Si no es POST, mostrar confirmación
    return render(request, "notificaciones/confirmar_eliminar_todas.html")
