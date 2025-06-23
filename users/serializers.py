from rest_framework import serializers
from .models import ApplicationUser

class ApplicationUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = [
            'id_aplicacion_usuario',
            'application',
            'username',
            'fecha_ini',
            'fecha_fin',
            'name',
            'provider',
            'provider_id',
            'remember_token',
            'estado_sesion',
            'fecha_validacion',
            'dni',
            'nombres',
            'apellidos',
            'estado_validacion',
            'pais',
            'refresh_token',
            'avatar',
            'password',
            'old_id',
            'fecha_purga',
        ]  # Los campos deben coincidir exactamente con el modelo
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Validar que no exista usuario repetido para la misma aplicación
        if ApplicationUser.objects.filter(
            application=data['application'],
            username=data['username']
        ).exists():
            raise serializers.ValidationError("Ya existe un usuario con ese username en la aplicación.")
        return data