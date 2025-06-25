from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from custom_auth.repositories.global_access_user_repository import crear_usuario_global, existe_email_o_np

class GlobalAccessUserCreateView(APIView):
    """
    Vista para registrar un nuevo usuario con acceso global a todos los centros de gestión.
    requiere np, nombre, email y usuario_creo. Inserta usuario global usando SQL directo.
    """
    def post(self, request):
        data = request.data
        np = data.get('np')
        nombre = data.get('nombre')
        email = data.get('email')
        usuario_creo = data.get('usuario_creo')

        # Validación básica
        if not np or not nombre or not email or not usuario_creo:
            return Response({'error': 'Todos los campos son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar unicidad
        if existe_email_o_np(email, np):
            return Response({'error': 'El email o número personal ya existe.'}, status=status.HTTP_400_BAD_REQUEST)

        # Insertar usuario
        try:
            crear_usuario_global(np, nombre, email, usuario_creo)
            return Response({'np': np, 'nombre': nombre, 'email': email, 'usuario_creo': usuario_creo}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Error al crear usuario: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
