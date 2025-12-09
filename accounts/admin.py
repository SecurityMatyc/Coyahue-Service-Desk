from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, Tecnico


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ("email", "first_name", "last_name", "rol", "is_active")
    list_filter = ("rol", "is_active")
    ordering = ("email",)
    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name", "telefono", "departamento")}),
        ("Rol y estado", {"fields": ("rol", "is_active", "is_staff", "is_superuser")}),
        ("Fechas", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "rol", "password1", "password2"),
        }),
    )


admin.site.register(Rol)
admin.site.register(Tecnico)
