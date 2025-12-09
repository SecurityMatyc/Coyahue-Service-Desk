from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Ticket, Categoria, Prioridad, EstadoTicket, AsignacionTicket, HistorialTicket
from .serializers import (
    TicketSerializer, CategoriaSerializer, PrioridadSerializer,
    EstadoTicketSerializer, AsignacionTicketSerializer, HistorialTicketSerializer
)
from .permissions import EsAdministrador, EsTecnico


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related("solicitante", "categoria", "prioridad", "estado")
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ticket = serializer.save(solicitante=self.request.user)
        HistorialTicket.objects.create(
            ticket=ticket,
            usuario=self.request.user,
            accion="creado",
            descripcion_cambio="Creación de ticket",
            datos_nuevos=serializer.data,
        )

    def get_queryset(self):
        user = self.request.user
        if user.rol.nombre_rol in ("ADMIN", "TECNICO"):
            return super().get_queryset()
        return super().get_queryset().filter(solicitante=user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, EsAdministrador])
    def asignar(self, request, pk=None):
        ticket = self.get_object()
        tecnico_id = request.data.get("tecnico_id")

        asignacion = AsignacionTicket.objects.create(
            ticket=ticket,
            usuario=request.user,
            tecnico_asignado_id=tecnico_id,
            comentario_asignacion=request.data.get("comentario", ""),
        )

        HistorialTicket.objects.create(
            ticket=ticket,
            usuario=request.user,
            accion="asignado",
            descripcion_cambio=f"Asignado al técnico {tecnico_id}",
            datos_nuevos={"tecnico_id": tecnico_id},
        )

        return Response(AsignacionTicketSerializer(asignacion).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def cambiar_estado(self, request, pk=None):
        ticket = self.get_object()
        estado_id = request.data.get("estado_id")
        estado_anterior = ticket.estado_id

        ticket.estado_id = estado_id
        ticket.save()

        HistorialTicket.objects.create(
            ticket=ticket,
            usuario=request.user,
            accion="cambio_estado",
            descripcion_cambio="Cambio de estado",
            datos_anteriores={"estado_id": estado_anterior},
            datos_nuevos={"estado_id": estado_id},
        )

        return Response(self.get_serializer(ticket).data)
