from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from .managers import UsuarioManager


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    permisos = models.JSONField(default=dict, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.nombre_rol


class Usuario(AbstractUser):
    """
    Usuario personalizado:
    - Login por email (USERNAME_FIELD = 'email')
    - Relación con Rol
    """

    # Eliminamos el username clásico
    username = None

    email = models.EmailField("email address", unique=True)

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name="usuarios",
        null=True,
        blank=True,
    )

    telefono = models.CharField(max_length=30, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    # Avatar personalizado (íconos predefinidos)
    AVATAR_CHOICES = [
        ('👤', '👤 Persona'),
        ('👨', '👨 Hombre'),
        ('👩', '👩 Mujer'),
        ('🧑', '🧑 Persona neutra'),
        ('👔', '👔 Profesional'),
        ('💼', '💼 Ejecutivo'),
        ('🎓', '🎓 Estudiante'),
        ('⚙️', '⚙️ Técnico'),
    ]
    avatar = models.CharField(
        max_length=10,
        choices=AVATAR_CHOICES,
        default='👤',
        help_text="Ícono de perfil personalizado"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []  # no pedimos username, solo email + password

    objects = UsuarioManager()

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        nombre = f"{self.first_name} {self.last_name}".strip()
        return nombre or self.email

    def get_absolute_url(self):
        return reverse("usuarios_editar", kwargs={"usuario_id": self.id})


class Tecnico(models.Model):
    """
    Perfil de técnico asociado a un Usuario con rol TÉCNICO.
    """

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="tecnico",
    )
    especialidad = models.CharField(max_length=100, blank=True)
    nivel_experiencia = models.CharField(max_length=50, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Técnico: {self.usuario.get_full_name()}"
