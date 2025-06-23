from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .repositories.centro_costo_repository import CentroCostoRepository

class CentroCostoListView(APIView):
    """
    Endpoint de solo lectura para listar centros de costo únicos desde el DW.
    """
    def get(self, request, *args, **kwargs):
        try:
            centros = CentroCostoRepository.listar_centros_costo()
            return Response(centros, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
