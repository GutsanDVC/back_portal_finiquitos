from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from settlements.services.kiptor_service import simulate_settlement_kiptor
from settlements.services.settlement_kiptor_utils import (
    parsear_datos, parsear_resultado, parsear_todo,parsear_body_for_kiptor
)
from settlements.repositories.settlement_repository import SettlementRepository
from warehouse.repositories.uf_repository import UfRepository

class KiptorSettlementSimulatorView(APIView):
    """
    Endpoint para simular el finiquito usando Kiptor.
    """

    def post(self, request):
        try:
            # 1. Parsear datos de entrada
            datos = parsear_datos(request.data)
            # 2. Calcular datos para finiquito
            resultado_finiquito = SettlementRepository.calcular_finiquito(datos)
            resultado_finiquito_parseado = parsear_resultado(resultado_finiquito)
            datos_uf=UfRepository.get_uf_by_date(datos['fecha_desvinculacion'])
            valor_uf=datos_uf['valor_uf']
            body=parsear_body_for_kiptor(datos,resultado_finiquito_parseado,valor_uf)
            # 3. Simular con Kiptor
            resultado_kiptor = simulate_settlement_kiptor(body)
            # 4. Combinar resultados y responder
            # respuesta = parsear_todo(request.data, resultado_finiquito_parseado, resultado_kiptor)
            respuesta = resultado_kiptor
            
            return Response(respuesta, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
