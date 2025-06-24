from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from custom_auth.serializers import GlobalAccessUserSerializer

class GlobalAccessUserCreateView(APIView):
    """
    Vista para registrar un nuevo usuario con acceso global a todos los centros de gestión.
    Solo requiere un email válido y único.
    """
    def post(self, request):
        serializer = GlobalAccessUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
