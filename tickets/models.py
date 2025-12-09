from django.db import models
from accounts.models import Usuario, Tecnico
from datetime import timedelta
from django.utils import timezone


class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_categoria


class Subcategoria(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="subcategorias",
    )
    nombre_subcategoria = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ("categoria", "nombre_subcategoria")

    def __str__(self):
        return f"{self.categoria.nombre_categoria} / {self.nombre_subcategoria}"


class Prioridad(models.Model):
    nombre_prioridad = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    nivel = models.PositiveSmallIntegerField(
        default=2,
        help_text="1=Baja, 2=Media, 3=Alta, 4=Crítica (o similar)."
    )

    # NUEVO: SLA por prioridad (en horas)
    sla_horas = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Horas objetivo de resolución para esta prioridad."
    )

    def __str__(self) -> str:
        return self.nombre_prioridad


class EstadoTicket(models.Model):
    """
    Ejemplos:
    - Abierto
    - En Progreso
    - Resuelto
    - Cerrado
    """
    nombre_estado = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    es_final = models.BooleanField(
        default=False,
        help_text="Indica si es un estado final (Resuelto, Cerrado)."
    )

    def __str__(self):
        return self.nombre_estado


class AreaAfectada(models.Model):
    """
    Ejemplos:
    - Finanzas
    - RRHH
    - TI
    - Ventas
    - Producción
    """
    nombre_area = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre_area


class Ticket(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    solicitante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="tickets_solicitados",
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    prioridad = models.ForeignKey(
        Prioridad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    area_afectada = models.ForeignKey(
        AreaAfectada,
        on_delete=models.PROTECT,
        related_name="tickets",
    )

    estado = models.ForeignKey(
        EstadoTicket,
        on_delete=models.PROTECT,
        related_name="tickets",
    )

    archivo = models.FileField(
        upload_to="tickets_adjuntos/",
        blank=True,
        null=True,
        help_text="Archivos adjuntos: imágenes, PDF, etc."
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    sla_horas_objetivo = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="SLA en horas, si aplica."
    )

    def __str__(self):
        return f"Ticket #{self.id} - {self.titulo}"
    
    @property
    def sla_deadline(self):
        """
        Fecha/hora límite de SLA según la prioridad.
        """
        if self.prioridad and self.prioridad.sla_horas:
            return self.fecha_creacion + timedelta(hours=self.prioridad.sla_horas)
        return None

    @property
    def sla_status(self):
        """
        Estado SLA simplificado:
        - SIN_SLA      → no tiene SLA configurado
        - EN_CURSO     → abierto, dentro del plazo
        - ADVERTENCIA  → abierto, cerca de vencer
        - VENCIDO      → abierto, plazo vencido
        - CUMPLIDO     → cerrado dentro de SLA
        - VENCIDO_CERR → cerrado pero fuera de SLA
        """
        deadline = self.sla_deadline
        if not deadline:
            return "SIN_SLA"

        now = timezone.now()

        # Si está en estado final
        if self.estado and self.estado.es_final and self.fecha_cierre:
            if self.fecha_cierre <= deadline:
                return "CUMPLIDO"
            else:
                return "VENCIDO_CERR"

        # Ticket abierto
        if now > deadline:
            return "VENCIDO"

        # Advertencia cuando queda menos del 25% del tiempo
        total_seg = (deadline - self.fecha_creacion).total_seconds()
        restantes_seg = (deadline - now).total_seconds()
        if total_seg > 0 and (restantes_seg / total_seg) <= 0.25:
            return "ADVERTENCIA"

        return "EN_CURSO"

    @property
    def sla_cumplido_bool(self):
        """
        True / False / None para métricas.
        """
        status = self.sla_status
        if status in ("CUMPLIDO",):
            return True
        if status in ("VENCIDO", "VENCIDO_CERR"):
            return False
        return None


class AsignacionTicket(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="asignaciones",
    )
    tecnico_asignado = models.ForeignKey(
        Tecnico,
        on_delete=models.CASCADE,
        related_name="tickets_asignados",
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Ticket #{self.ticket.id} asignado a {self.tecnico_asignado.usuario.email}"


class HistorialTicket(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="historial",
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acciones_ticket",
    )
    estado_anterior = models.ForeignKey(
        EstadoTicket,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="historial_antes",
    )
    estado_nuevo = models.ForeignKey(
        EstadoTicket,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="historial_despues",
    )

    comentario = models.TextField(blank=True)
    fecha_accion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historial Ticket #{self.ticket.id} ({self.fecha_accion})"


class ComentarioTicket(models.Model):
    """
    Comentarios que usuarios, técnicos y admins pueden agregar a un ticket
    para comunicación bidireccional.
    """
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
    texto = models.TextField(
        help_text="Contenido del comentario"
    )
    archivo = models.FileField(
        upload_to='comentarios/%Y/%m/',
        blank=True,
        null=True,
        help_text="Archivo adjunto opcional (imagen, PDF, etc.)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha_creacion']
        verbose_name = "Comentario de Ticket"
        verbose_name_plural = "Comentarios de Tickets"

    def __str__(self):
        usuario_nombre = self.usuario.get_full_name() or self.usuario.email
        return f"Comentario de {usuario_nombre} en Ticket #{self.ticket.id}"


class CalificacionTicket(models.Model):
    """
    Calificación de satisfacción (CSAT) que el usuario da cuando un ticket se cierra.
    Solo el usuario solicitante puede calificar su propio ticket, una sola vez.
    """
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name="calificacion",
        help_text="Ticket calificado (relación 1 a 1)"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        help_text="Usuario que realizó la calificación"
    )
    puntuacion = models.PositiveSmallIntegerField(
        choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')],
        help_text="Calificación de 1 a 5 estrellas"
    )
    resuelto = models.BooleanField(
        help_text="¿El problema fue resuelto?"
    )
    comentario = models.TextField(
        blank=True,
        help_text="Comentario adicional sobre la atención (opcional)"
    )
    fecha_calificacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Calificación de Ticket"
        verbose_name_plural = "Calificaciones de Tickets"
        ordering = ['-fecha_calificacion']

    def __str__(self):
        return f"Calificación {self.puntuacion}⭐ - Ticket #{self.ticket.id}"
