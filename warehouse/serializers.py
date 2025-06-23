from rest_framework import serializers
from .models import SapMaestroColaborador

class SapMaestroColaboradorSerializer(serializers.ModelSerializer):
    """
    Serializador para exponer los datos de SapMaestroColaborador vía API REST.
    """
    class Meta:
        model = SapMaestroColaborador
        fields = '__all__'
