from django.contrib import admin
from .models import Notificacion, EventoCritico


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "usuario_destino", "tipo_notificacion",
                    "leida", "canal_notificacion", "fecha_envio")
    list_filter = ("tipo_notificacion", "leida", "canal_notificacion")
    search_fields = ("titulo", "mensaje", "usuario_destino__email", "ticket__titulo")


@admin.register(EventoCritico)
class EventoCriticoAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo_evento", "nivel_gravedad",
                    "resuelto", "fecha_deteccion", "fecha_resolucion")
    list_filter = ("nivel_gravedad", "resuelto")
