from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .repositories.colaborador_repository import ColaboradorRepository

class SapMaestroColaboradorListView(APIView):
    """
    Endpoint de solo lectura para listar colaboradores del Data Warehouse (SQL directo).
    Permite filtrar por centro de costo usando el parámetro ?centro_costo=XXX.
    Si no hay filtro de centro_costo, aplica paginación (?page, ?page_size).
    """
    def get(self, request, *args, **kwargs):
        centros_costos = request.query_params.getlist('centros_costos', [])
        ver_planta = request.query_params.get('ver_planta') or None
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 500))
            total_count = ColaboradorRepository.total_colaboradores()
            colaboradores = ColaboradorRepository.listar_colaboradores(centro_costo=centros_costos,ver_planta=ver_planta,page=page, page_size=page_size)
            res= {
                'results': colaboradores,
                'page': page,
                'page_size':  page_size,
                'total_count': total_count,
                'total_pages': int(total_count / page_size) + (1 if total_count % page_size > 0 else 0)
            }

            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            # Retorna error genérico y mensaje para debug
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ColaboradorPorCorreoView(APIView):
    """
    Endpoint para buscar un colaborador específico por su correo electrónico.
    Requiere el parámetro 'correo' en la URL como query parameter.
    """
    def get(self, request, *args, **kwargs):
        correo_flesan = request.query_params.get('correo')
        
        if not correo_flesan:
            return Response(
                {'detail': 'El parámetro "correo" es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            colaborador = ColaboradorRepository.buscar_colaborador_por_correo(correo_flesan)
            
            if colaborador:
                return Response(colaborador, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'detail': 'No se encontró ningún colaborador con el correo proporcionado'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            # Retorna error genérico y mensaje para debug
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExternalCode162ListView(APIView):
    """

    """
    def get(self, request, *args, **kwargs):
        try:
            external_code_162 = ColaboradorRepository.external_code_162()
            return Response(external_code_162, status=status.HTTP_200_OK)
        except Exception as e:
            # Retorna error genérico y mensaje para debug
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompensacionPorNpView(APIView):
    """
    Endpoint para obtener el sueldo base y valor de hora extra de un colaborador por su NP.
    Requiere el parámetro 'np' en la URL como query parameter.
    """
    def get(self, request, *args, **kwargs):
        np = request.query_params.get('np')
        
        if not np:
            return Response(
                {'detail': 'El parámetro "np" es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar que np sea un número
        try:
            np = int(np)
        except (ValueError, TypeError):
            return Response(
                {'detail': 'El parámetro "np" debe ser un número válido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            compensacion = ColaboradorRepository.obtener_compensacion_por_np(np)
            
            if compensacion:
                return Response(compensacion, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'detail': f'No se encontró información de compensación para el NP {np}'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            # Retorna error genérico y mensaje para debug
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
