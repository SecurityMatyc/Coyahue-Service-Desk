from django.contrib.auth.models import BaseUserManager
from django.apps import apps


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def get_rol_model(self):
        return apps.get_model("accounts", "Rol")

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Debe ingresar email")

        email = self.normalize_email(email)

        # Convertir rol numérico/string en instancia correcta
        rol_model = self.get_rol_model()
        rol = extra_fields.get("rol")

        if isinstance(rol, (int, str)):
            extra_fields["rol"] = rol_model.objects.get(pk=rol)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("activo", True)

        return self.create_user(email, password, **extra_fields)
