from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Usuario, Tecnico


@receiver(post_save, sender=Usuario)
def crear_o_actualizar_tecnico(sender, instance, created, **kwargs):
    # Solo aplica a usuarios con rol TECNICO
    if not instance.rol:
        return

    rol_nombre = instance.rol.nombre_rol.upper()

    if rol_nombre == "TECNICO":
        # Si se acaba de crear el usuario técnico, crear perfil Tecnico
        if created:
            Tecnico.objects.get_or_create(usuario=instance)
        else:
            # Usuario ya existía, asegurar que tenga perfil Tecnico
            Tecnico.objects.get_or_create(usuario=instance)
    else:
        # Si dejó de ser técnico, opcionalmente podrías borrar su perfil técnico:
        # Tecnico.objects.filter(usuario=instance).delete()
        pass
