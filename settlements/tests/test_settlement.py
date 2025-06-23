"""
Pruebas unitarias para el cálculo de finiquito en settlements.
"""
import pytest
from settlements.services.settlement_calculator import calculate_settlement

def test_calculate_settlement_single():
    empleado = {
        "np": 1,
        "sueldo_base": 500000,
        "colacion": 30000,
        "vacaciones": 120000
    }
    resultado = calculate_settlement(empleado)
    assert isinstance(resultado, list)
    assert resultado[0]["np"] == 1
    assert resultado[0]["base"] == 500000
    assert resultado[0]["gratificacion"] == 125000
    assert resultado[0]["colacion"] == 30000
    assert resultado[0]["vacaciones"] == 120000

def test_calculate_settlement_multiple():
    empleados = [
        {"np": 1, "sueldo_base": 500000, "colacion": 30000, "vacaciones": 120000},
        {"np": 2, "sueldo_base": 600000, "colacion": 35000, "vacaciones": 150000}
    ]
    resultado = calculate_settlement(empleados)
    assert len(resultado) == 2
    assert resultado[1]["np"] == 2
    assert resultado[1]["base"] == 600000
    assert resultado[1]["gratificacion"] == 150000
    assert resultado[1]["colacion"] == 35000
    assert resultado[1]["vacaciones"] == 150000
