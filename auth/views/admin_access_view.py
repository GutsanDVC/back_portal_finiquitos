from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from auth.services.admin_access_service import AdminAccessService

class AdminAccessView(APIView):
    """
    Endpoint para obtener accesos administrativos por correo.
    """
    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'El parámetro email es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        data = AdminAccessService.get_admin_access(email)
        return Response(data, status=status.HTTP_200_OK)
