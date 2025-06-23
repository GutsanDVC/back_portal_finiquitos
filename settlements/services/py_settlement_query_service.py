"""
Servicio para ejecutar la query de cálculo de finiquito parametrizada para Python.

- Lee la query desde el archivo calculo_finiquito_py.sql
- Ejecuta la consulta usando una conexión estándar (psycopg2, etc.)
- Retorna los resultados como lista de diccionarios.

Uso recomendado:
    from py_settlement_query_service import calculate_settlement
    import psycopg2

    conn = psycopg2.connect(...)
    params = {
        'np': 12345,
        'fecha_desvinculacion': '2024-06-01',
        'tipo_solicitud': 'R',
        'grat': 100000.0
        # ...otros parámetros necesarios
    }
    resultados = calculate_settlement(params, conn)
"""
import os

# Librería estándar para convertir resultados de cursor a diccionario
from typing import List, Dict, Any

def load_query() -> str:
    """
    Carga la query SQL parametrizada desde el archivo calculo_finiquito_py.sql.
    """
    ruta = os.path.join(
        os.path.dirname(__file__),
        '..', 'query', 'calculo_finiquito.sql'
    )
    with open(ruta, encoding='utf-8') as f:
        return f.read()

def calculate_settlement(params: Dict[str, Any], connection) -> List[Dict[str, Any]]:
    """
    Ejecuta la query de cálculo de finiquito con los parámetros entregados.

    Args:
        params: Diccionario con los parámetros requeridos por la query.
        connection: Conexión activa a la base de datos (psycopg2, etc.).
    Returns:
        Lista de diccionarios con los resultados.
    """
    query = load_query()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        # Obtener nombres de columnas
        columns = [desc[0] for desc in cursor.description]
        # Retornar resultados como lista de diccionarios
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Nota: Este servicio asume que la conexión es gestionada por el llamador
# y que los parámetros coinciden con los definidos en el SQL.
