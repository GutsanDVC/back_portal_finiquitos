from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from warehouse.repositories.causal_termino_repository import CausalTerminoRepository

class CausalTerminoListView(APIView):
    """
    Vista para listar las causales de término.
    """
    def get(self, request):
        try:
            causales = CausalTerminoRepository.listar_causales_termino()
            return Response(causales, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
