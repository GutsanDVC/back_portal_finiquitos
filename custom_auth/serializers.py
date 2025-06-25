from rest_framework import serializers
from .models import GlobalAccessUser

class GlobalAccessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalAccessUser
        # Incluimos todos los campos relevantes
        fields = ["np", "nombre", "email", "usuario_creo", "created_at"]
        extra_kwargs = {
            "np": {"required": True},
            "nombre": {"required": True},
            "email": {"required": True},
            "usuario_creo": {"required": True},
        }

    def validate_email(self, value):
        # Valida que el email no exista ya en el modelo
        if GlobalAccessUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo ya tiene acceso global.")
        return value

    def validate_np(self, value):
        # Valida que el np (número personal) sea único
        if GlobalAccessUser.objects.filter(np=value).exists():
            raise serializers.ValidationError("El número personal ya existe.")
        return value
