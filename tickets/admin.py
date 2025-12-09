# Register your models here.
from django.contrib import admin
from .models import (
    Categoria,
    Subcategoria,
    Prioridad,
    EstadoTicket,
    Ticket,
    AsignacionTicket,
    HistorialTicket,
    ComentarioTicket,
    CalificacionTicket,
)


admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Prioridad)
admin.site.register(EstadoTicket)
admin.site.register(Ticket)
admin.site.register(AsignacionTicket)
admin.site.register(HistorialTicket)
admin.site.register(ComentarioTicket)
admin.site.register(CalificacionTicket)

