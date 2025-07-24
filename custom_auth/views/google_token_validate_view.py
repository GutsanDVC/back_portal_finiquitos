from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from custom_auth.services.auth_service import google_validate_id_token
from django.core.exceptions import ValidationError
from custom_auth.services.admin_access_service import AdminAccessService
from custom_auth.services.auth_service import parsear_admin_access,parsear_global_access

class GoogleTokenValidateView(APIView):
    """
    Endpoint para validar un id_token de Google.
    """
    def post(self, request):
        id_token = request.data.get("id_token")
        if not id_token:
            return Response({"error": "El campo id_token es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_data = google_validate_id_token(id_token=id_token)
            email = user_data.get("email")
            admin_access = AdminAccessService.get_admin_access(email)
            if admin_access[0].get("global_access"):
                data = parsear_global_access(user_data)
            else:
                data = parsear_admin_access(admin_access,user_data)
            if not admin_access:
                response = {
                    "valid": False,
                    "data": data,
                    "message": 'El usuario no tiene obras para administrar.'
                }
            else:
                
                response = {
                    "valid": True,
                    "data": data,
                    "message": 'El usuario tiene obras para administrar.'
                }
            response['data']['global_access']=True if admin_access[0].get("global_access") else False    
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Error interno.", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
