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
