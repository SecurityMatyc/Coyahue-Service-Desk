# Create your models here.
from django.db import models
from django.conf import settings
from tickets.models import Ticket

Usuario = settings.AUTH_USER_MODEL


class Notificacion(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="notificaciones", null=True, blank=True)
    usuario_destino = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="notificaciones"
    )
    tipo_notificacion = models.CharField(max_length=50)  # creacion, asignacion, cambio_estado...
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    canal_notificacion = models.CharField(max_length=50, default="portal")  # portal, correo, etc.

    def __str__(self):
        return f"Notif {self.tipo_notificacion} -> {self.usuario_destino}"


class EventoCritico(models.Model):
    tipo_evento = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_deteccion = models.DateTimeField()
    nivel_gravedad = models.CharField(max_length=20)
    resuelto = models.BooleanField(default=False)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.tipo_evento
