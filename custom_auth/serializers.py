from rest_framework import serializers
from .models import GlobalAccessUser

class GlobalAccessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalAccessUser
        fields = ["email"]
        extra_kwargs = {"email": {"required": True}}

    def validate_email(self, value):
        # Valida que el email no exista ya en el modelo
        if GlobalAccessUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo ya tiene acceso global.")
        return value
