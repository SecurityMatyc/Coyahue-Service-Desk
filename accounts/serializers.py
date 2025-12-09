from rest_framework import serializers
from .models import Usuario, Rol, Tecnico

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(), source="rol", write_only=True
    )

    class Meta:
        model = Usuario
        fields = [
            "id", "email", "first_name", "last_name",
            "telefono", "departamento", "activo",
            "rol", "rol_id",
        ]


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["email", "first_name", "last_name", "password", "rol"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TecnicoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), source="usuario", write_only=True
    )

    class Meta:
        model = Tecnico
        fields = [
            "id", "usuario", "usuario_id",
            "especialidad", "carga_trabajo_actual",
            "disponible", "calificacion_promedio",
        ]