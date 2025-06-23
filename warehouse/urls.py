from django.urls import path
from .views import SapMaestroColaboradorListView
from .views_centro_costo import CentroCostoListView

urlpatterns = [
    path('colaboradores/', SapMaestroColaboradorListView.as_view(), name='warehouse-colaboradores-list'),
    path('centros-costo/', CentroCostoListView.as_view(), name='warehouse-centros-costo-list'),
]
