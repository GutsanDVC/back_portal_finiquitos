from django.urls import path
from .views import CalculoSueldoLiquidoView, CalculoSueldoBrutoDesdeNeto

urlpatterns = [
    path('calculo-sueldo-liquido/', CalculoSueldoLiquidoView.as_view(), name='salary-calculo-sueldo-liquido'),
    path('calculo-sueldo-bruto-desde-neto/', CalculoSueldoBrutoDesdeNeto.as_view(), name='salary-calculo-sueldo-bruto-desde-neto'),
]
