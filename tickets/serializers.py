from rest_framework import serializers
from .models import (
    Ticket, Categoria, Subcategoria, Prioridad,
    EstadoTicket, AsignacionTicket, HistorialTicket,
)

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoria
        fields = "__all__"


class PrioridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prioridad
        fields = "__all__"


class EstadoTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoTicket
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    solicitante = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ["solicitante", "fecha_creacion", "fecha_actualizacion", "fecha_cierre"]


class AsignacionTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignacionTicket
        fields = "__all__"


class HistorialTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialTicket
        fields = "__all__"

