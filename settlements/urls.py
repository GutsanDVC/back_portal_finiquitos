from django.urls import path
from .views import SettlementCalculationView, SettlementCalculationMasivoView
from .views_kiptor_simulator import KiptorSettlementSimulatorView

urlpatterns = [
    path('calculate/', SettlementCalculationView.as_view(), name='settlement-calculate'),
    path('calculate/masivo/', SettlementCalculationMasivoView.as_view(), name='settlement-calculate-masivo'),
    path('simulate-kiptor-settlement/', KiptorSettlementSimulatorView.as_view(), name='simulate-kiptor-settlement'),
]
