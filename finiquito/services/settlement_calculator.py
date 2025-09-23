"""
Servicio principal para el cálculo de finiquito.
Recibe uno o varios empleados en formato dict y retorna el resultado del cálculo para cada uno.
"""
from settlements.utils.helpers import calcular_gratificacion, calcular_base, calcular_colacion, calcular_vacaciones


def calculate_settlement(employees):
    """
    Calcula el finiquito para uno o varios empleados.
    :param employees: list[dict] o dict (un solo empleado)
    :return: list[dict] resultados del cálculo
    """
    if isinstance(employees, dict):
        employees = [employees]
    resultados = []
    for empleado in employees:
        # Ejemplo: se pueden agregar más campos según lógica PHP
        base = calcular_base(empleado)
        gratificacion = calcular_gratificacion(empleado, base)
        colacion = calcular_colacion(empleado)
        vacaciones = calcular_vacaciones(empleado)
        resultado = {
            "np": empleado.get("np"),
            "base": base,
            "gratificacion": gratificacion,
            "colacion": colacion,
            "vacaciones": vacaciones,
            # ...otros conceptos y cálculos
        }
        resultados.append(resultado)
    return resultados
