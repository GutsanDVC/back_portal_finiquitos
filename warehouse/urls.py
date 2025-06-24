from django.urls import path
from .views import SapMaestroColaboradorListView
from .views_centro_costo import CentroCostoListView
from .causal_termino_view import CausalTerminoListView

urlpatterns = [
    path('colaboradores/', SapMaestroColaboradorListView.as_view(), name='warehouse-colaboradores-list'),
    path('centros-costo/', CentroCostoListView.as_view(), name='warehouse-centros-costo-list'),
    path('causales-termino/', CausalTerminoListView.as_view(), name='warehouse-causales-termino-list'),
]
