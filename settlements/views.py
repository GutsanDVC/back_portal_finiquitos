from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from settlements.repositories.settlement_repository import SettlementRepository

class SettlementCalculationView(APIView):
    """
    Vista para calcular el finiquito de uno o varios empleados consultando directamente el Data Warehouse (DW).

    POST /api/settlements/calculate/

    Request:
    [
      {
        "np": 1234,
        "fecha_desvinculacion": "2024-06-01",
        "tipo_solicitud": "R",
        "grat": 100000.0
        // ...otros campos requeridos por la query SQL
      },
      ...
    ]

    Response:
    [
      {
        "np": 1234,
        "base": 500000,
        "gratificacion": 125000,
        "colacion": 30000,
        "vacaciones": 120000
        // ...otros conceptos calculados por la consulta SQL
      },
      ...
    ]
    Notas:
    - Cada entrada del request debe contener los parámetros necesarios para la consulta SQL de finiquito.
    - Si no existen resultados para un empleado, se retorna {"np": <valor>, "detalle": "Sin resultados"}.
    - La lógica de cálculo y obtención de datos se realiza 100% en el DW vía SQL parametrizado.
    """
    def post(self, request, *args, **kwargs):
        empleados = request.data
        try:
            resultado = []
            for params in empleados:
                res = SettlementRepository.calcular_finiquito(params)
                # Si la consulta no retorna nada, devolver un dict con np y detalle
                resultado.append(res if res else {"np": params.get("np"), "detalle": "Sin resultados"})
            return Response(resultado, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SettlementCalculationMasivoView(APIView):
    def post(self, request, *args, **kwargs):
        empleados = request.data
        try:
            # Llama al método batch con la lista completa
            res = SettlementRepository.calcular_finiquito_masivo(empleados)
            # Si algún empleado no tiene resultado, agregar el dict de "Sin resultados"
            nps_con_resultado = {r['numero_de_personal'] for r in res}
            resultado = []
            for emp in empleados:
                if str(emp['np']) in nps_con_resultado:
                    # Filtra todos los resultados para ese np
                    resultado.extend([r for r in res if str(r['numero_de_personal']) == str(emp['np'])])
                else:
                    resultado.append({"np": emp['np'], "detalle": "Sin resultados"})
            return Response(resultado, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



