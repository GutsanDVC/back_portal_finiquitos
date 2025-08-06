from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from custom_auth.repositories.global_access_user_repository import (
    crear_usuario_global,
    obtener_usuarios_globales,
    obtener_usuario_por_np,
    actualizar_usuario_global,
    eliminar_usuario_global,
    existe_email_o_np
)

class GlobalAccessUserListCreateView(APIView):
    """
    GET: Lista todos los usuarios globales.
    POST: Crea un usuario global.
    """
    def get(self, request):
        usuarios = obtener_usuarios_globales()
        return Response(usuarios, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        np = data.get('np')
        nombre = data.get('nombre')
        email = data.get('email')
        # Usar valores por defecto solo si el campo no está presente (None)
        activo = data.get('activo', True)  # True por defecto si no se especifica
        ver_nfg = data.get('ver_nfg', False)  # False por defecto si no se especifica
        email=email.lower()
        usuario_creo = data.get('usuario_creo')
        if not np or not nombre or not email or not usuario_creo:
            return Response({'error': 'Todos los campos son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)
        if existe_email_o_np(email, np):
            return Response({'error': 'El email o número personal ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            crear_usuario_global(np, nombre, email, usuario_creo,activo,ver_nfg)
            return Response({'np': np, 'nombre': nombre, 'email': email, 'usuario_creo': usuario_creo}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Error al crear usuario: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GlobalAccessUserDetailView(APIView):
    """
    GET: Obtiene un usuario global por np.
    PUT: Actualiza un usuario global por np.
    DELETE: Elimina un usuario global por np.
    """
    def get(self, request, np):
        usuario = obtener_usuario_por_np(np)
        if usuario:
            return Response(usuario, status=status.HTTP_200_OK)
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, np):
        data = request.data
        nombre = data.get('nombre')
        email = data.get('email')
        usuario_creo = data.get('usuario_creo')
        # Usar valores por defecto solo si el campo no está presente (None)
        activo = data.get('activo', True)  # True por defecto si no se especifica
        ver_nfg = data.get('ver_nfg', False)  # False por defecto si no se especifica
        email=email.lower()
        if not (nombre or email or usuario_creo):
            return Response({'error': 'Debe indicar al menos un campo a actualizar.'}, status=status.HTTP_400_BAD_REQUEST)
        # Si se va a actualizar el email o np, validar unicidad
        if email or np:
            usuario_existente = obtener_usuario_por_np(np)
            if not usuario_existente:
                return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            if email and email != usuario_existente['email'] and existe_email_o_np(email, np):
                return Response({'error': 'El email ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
        actualizado = actualizar_usuario_global(np, nombre=nombre, email=email, usuario_creo=usuario_creo,activo=activo,ver_nfg=ver_nfg)
        if actualizado:
            return Response({'message': 'Usuario actualizado correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No se pudo actualizar el usuario.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, np):
        eliminado = eliminar_usuario_global(np)
        if eliminado:
            return Response({'message': 'Usuario eliminado correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
