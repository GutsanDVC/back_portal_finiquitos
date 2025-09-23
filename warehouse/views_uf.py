from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from warehouse.repositories.uf_repository import UfRepository

class UfByDateView(APIView):
    """
    Endpoint para obtener el valor de la UF según una fecha dada.
    Recibe un parámetro 'fecha' por query string (YYYY-MM-DD).
    """
    def get(self, request):
        fecha = request.query_params.get('fecha')
        if not fecha:
            return Response({'error': 'El parámetro fecha es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        uf = UfRepository.get_uf_by_date(fecha)
        if uf:
            return Response(uf, status=status.HTTP_200_OK)
        return Response({'error': 'No se encontró UF para la fecha proporcionada.'}, status=status.HTTP_404_NOT_FOUND)
class UtmUfByDateView(APIView):
    """
    Endpoint para obtener el valor de la UTM y UF según una fecha dada.
    Recibe un parámetro 'fecha' por query string (YYYY-MM-DD).
    """
    def get(self, request):
        fecha = request.query_params.get('fecha')
        if not fecha:
            return Response({'error': 'El parámetro fecha es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        uf = UfRepository.get_utm_uf_by_date(fecha)
        if uf:
            return Response(uf, status=status.HTTP_200_OK)
        return Response({'error': 'No se encontró UTM para la fecha proporcionada.'}, status=status.HTTP_404_NOT_FOUND)