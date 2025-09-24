from django.urls import path
from .views import SapMaestroColaboradorListView, ExternalCode162ListView, ColaboradorPorCorreoView, CompensacionPorNpView
from .views_centro_costo import CentroCostoListView
from .causal_termino_view import CausalTerminoListView
from .views_uf import UfByDateView, UtmUfByDateView

urlpatterns = [
    path('colaboradores/', SapMaestroColaboradorListView.as_view(), name='warehouse-colaboradores-list'),
    path('colaborador-por-correo/', ColaboradorPorCorreoView.as_view(), name='warehouse-colaborador-por-correo'),
    path('compensacion-por-np/', CompensacionPorNpView.as_view(), name='warehouse-compensacion-por-np'),
    path('centros-costo/', CentroCostoListView.as_view(), name='warehouse-centros-costo-list'),
    path('causales-termino/', CausalTerminoListView.as_view(), name='warehouse-causales-termino-list'),
    path('external-code-162/', ExternalCode162ListView.as_view(), name='warehouse-external-code-162-list'),
    # Endpoint para consultar el valor de la UF según una fecha dada
    path('uf/', UfByDateView.as_view(), name='warehouse-uf-by-date'),
    path('utm-uf/', UtmUfByDateView.as_view(), name='warehouse-utm-uf-by-date'),
]
