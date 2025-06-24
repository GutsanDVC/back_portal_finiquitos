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
        centro_costo = request.query_params.get('centro_costo') or None
        ver_planta = request.query_params.get('ver_planta') or None
        try:
            if centro_costo:
                colaboradores = ColaboradorRepository.listar_colaboradores(centro_costo=centro_costo,ver_planta=ver_planta)
                res= {
                    'results': colaboradores,
                    'page': 1,
                    'page_size':  len(colaboradores),
                    'total_count': len(colaboradores),
                    'total_pages': 1
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                # Paginación solo cuando no hay filtro
                page = int(request.query_params.get('page', 1))
                page_size = int(request.query_params.get('page_size', 500))
                colaboradores = ColaboradorRepository.listar_colaboradores(page=page, page_size=page_size)

                # Para total_count, se consulta el total sin paginación usando el repositorio
                total_count = ColaboradorRepository.total_colaboradores()
                res= {
                    'results': colaboradores,
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': int(total_count / page_size) + (1 if total_count % page_size > 0 else 0)
                }
                return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            # Retorna error genérico y mensaje para debug
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
