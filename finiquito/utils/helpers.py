"""
Funciones auxiliares para el cálculo de finiquito.

"""

import datetime

# Constante de gratificación legal (ajustar según reglas vigentes)
GRATIFICACION_MINIMA = 202127


def calcular_base(empleado):
    """
    Calcula el sueldo base del empleado.
    Si el concepto viene como 'base' en los datos, se utiliza ese valor.
    """
    # En el PHP, el sueldo base puede venir de un concepto específico.
    base = empleado.get("base")
    if base is not None:
        return int(base)
    # Fallback a sueldo_base si existe
    return int(empleado.get("sueldo_base", 0))


def calcular_gratificacion(empleado, base):
    """
    Calcula la gratificación legal según reglas del PHP.
    Si el cálculo imponible supera la gratificación mínima legal, se usa el mínimo.
    """
    # En el PHP, se compara el cálculo con la constante de gratificación
    grat = int(empleado.get("gratificacion", 0))
    if grat > 0:
        return grat
    # Fórmula: gratificación = 25% del base, tope en GRATIFICACION_MINIMA
    calculada = int(base * 0.25)
    return min(calculada, GRATIFICACION_MINIMA)


def calcular_colacion(empleado):
    """
    Calcula el monto de colación.
    Busca el concepto 'colacion' en los datos del empleado.
    """
    return int(empleado.get("colacion", 0))


def calcular_vacaciones(empleado):
    """
    Calcula el monto de vacaciones proporcionales.
    Puede usar campos como 'vacaciones', 'ponderacion_vacaciones', etc.
    """
    vacaciones = empleado.get("vacaciones")
    if vacaciones is not None:
        return int(vacaciones)
    # Si hay ponderación y base, calcular proporcional
    ponderacion = empleado.get("ponderacion_vacaciones")
    base = calcular_base(empleado)
    if ponderacion and base:
        # Ejemplo: vacaciones proporcionales = base * ponderacion / 30
        try:
            return int(base * float(ponderacion) / 30)
        except Exception:
            pass
    return 0
