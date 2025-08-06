from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from log.log_finiquitos_repository import crear_log_finiquito


class SettlementLogView(APIView):
    """
    Endpoint para crear logs de finiquitos.
    Recibe la información del log y la guarda usando el repository.
    """

    def post(self, request):
        """
        Crea un nuevo log de finiquito.
        
        Body esperado:
        {
            "user": "usuario@ejemplo.com",  // Opcional, si no se envía usa request.user.username
            "log_accion": {
                "accion": "simulacion_finiquito",
                "np": "123456",
                "fecha_desvinculacion": "2025-08-06",
                "resultado_finiquito": {...},
                "resultado_kiptor": {...},
                // ... otros campos relevantes
            }
        }
        """
        try:
            data = request.data
            # Obtener el usuario (usar el del request si no se especifica)
            user = data.get('user', request.user.username if hasattr(request.user, 'username') else 'anonymous')
            # Obtener la acción del log
            log_accion = data.get('log_accion')
            
            # Validar que se proporcione log_accion
            if not log_accion:
                return Response(
                    {'error': 'El campo "log_accion" es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar que log_accion sea un diccionario
            if not isinstance(log_accion, dict):
                return Response(
                    {'error': 'El campo "log_accion" debe ser un objeto JSON'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Crear el log usando el repository
            log_id = crear_log_finiquito(user, log_accion)
            return Response(
                {
                    'message': 'Log de finiquito creado exitosamente',
                    'log_id': log_id,
                    'user': user
                }, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            print(e)
            return Response(
                {'error': f'Error al crear el log: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
