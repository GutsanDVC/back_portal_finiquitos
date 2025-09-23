"""
Repository para ejecutar el cálculo de finiquito usando SQL directo contra el DW.
Utiliza psycopg2 y credenciales desde variables de entorno, siguiendo el patrón de ColaboradorRepository.
"""
import os
import psycopg2
from typing import List, Dict, Any

class SettlementRepository:
    """
    Repository para consultar el cálculo de finiquito desde el DW.
    """
    @staticmethod
    def get_connection():
        """
        Obtiene una conexión al Data Warehouse usando variables de entorno.
        """
        return psycopg2.connect(
            dbname=os.getenv('DB_NAME_DW'),
            user=os.getenv('DB_USER_DW'),
            password=os.getenv('DB_PASSWORD_DW'),
            host=os.getenv('DB_HOST_DW'),
            port=os.getenv('DB_PORT_DW')
        )

    @staticmethod
    def calcular_finiquito(params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Ejecuta la query de cálculo de finiquito con los parámetros entregados.
        Args:
            params: Diccionario con los parámetros requeridos por la query.
        Returns:
            Lista de diccionarios con los resultados.
        """
        # Ruta relativa al archivo SQL parametrizado
        ruta_sql = os.path.join(
            os.path.dirname(__file__),
            '..', 'query', 'calculo_finiquito_py.sql'
        )
        with open(ruta_sql, encoding='utf-8') as f:
            query = f.read()
        with SettlementRepository.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def calcular_finiquito_masivo(empleados: list) -> list:
        """
        Ejecuta el cálculo de finiquito para múltiples empleados en una sola consulta batch.
        Args:
            empleados: Lista de diccionarios, cada uno con las claves 'np', 'fecha_desvinculacion', 'tipo_solicitud', 'grat'.
        Returns:
            Lista de diccionarios con los resultados para todos los empleados.
        """
        # Ruta al archivo SQL batch
        ruta_sql = os.path.join(
            os.path.dirname(__file__),
            '..', 'query', 'calculo_finiquito_batch.sql'
        )
        with open(ruta_sql, encoding='utf-8') as f:
            query_template = f.read()
        # Construir VALUES y parámetros dinámicamente
        values_sql = []
        params = {}
        for idx, emp in enumerate(empleados):
            i = idx + 1
            values_sql.append(f"(%(np_{i})s, %(fecha_desvinculacion_{i})s, %(tipo_solicitud_{i})s, %(grat)s)")
            params[f'np_{i}'] = emp['np']
            params[f'fecha_desvinculacion_{i}'] = emp['fecha_desvinculacion']
            params[f'tipo_solicitud_{i}'] = emp['tipo_solicitud']
            # grat es igual para todos, se toma el del primero
            params['grat'] = emp['grat']
        values_clause = ',\n        '.join(values_sql)
        # Reemplazar el bloque de comentarios por el VALUES generado
        query = query_template.replace(
            "-- Python debe generar dinámicamente las filas:\n        -- (%(np_1)s, %(fecha_desvinculacion_1)s, %(tipo_solicitud_1)s, %(grat)s),\n        -- (%(np_2)s, %(fecha_desvinculacion_2)s, %(tipo_solicitud_2)s, %(grat)s)\n        -- ...",
            values_clause
        )
        # Ejecutar la consulta batch
        with SettlementRepository.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
