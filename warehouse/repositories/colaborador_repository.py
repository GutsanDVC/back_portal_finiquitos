import psycopg2
import os
from django.conf import settings
from utils.dw_utils import DWConnectionUtils

class ColaboradorRepository:
    """
    Repository para consultar colaboradores desde el DW usando SQL directo.
    Utiliza psycopg2 y credenciales desde variables de entorno/configuración.
    """

    @staticmethod
    def total_colaboradores():
        """
        Retorna el total de colaboradores en la tabla.
        """
        sql = DWConnectionUtils.sql_load('warehouse', 'total_colaboradores.sql')
        result = DWConnectionUtils.fetch_dicts(sql)
        return result[0]['total_count'] if result else 0

    @staticmethod
    def listar_colaboradores(centro_costo=None, page=None, page_size=None):
        """
        Retorna una lista de dicts con los colaboradores. Si se pasa centro_costo, filtra por ese campo.
        Si no se pasa centro_costo, aplica paginación usando page y page_size.
        """
        # Cargar la query desde archivo usando la utilidad
        sql = DWConnectionUtils.sql_load('warehouse', 'listar_colaboradores.sql')
        params = []
        if centro_costo:
            sql += ' AND centro_costo like %s'
            params.append('%' + centro_costo + '%')
        else:
            # Solo paginar si no hay filtro de centro_costo
            if page is not None and page_size is not None:
                offset = (page - 1) * page_size
                sql += ' OFFSET %s LIMIT %s'
                params.extend([offset, page_size])
        # Usar la utilidad general para ejecutar la consulta y obtener los resultados
        return DWConnectionUtils.fetch_dicts(sql, params)
