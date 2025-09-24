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
    def listar_colaboradores(centro_costo:list, page=None, page_size=None,ver_planta=None,user_admin_access=None):
        """
        Retorna una lista de dicts con los colaboradores. Si se pasa centro_costo, filtra por ese campo.
        Si no se pasa centro_costo, aplica paginación usando page y page_size.
        """
        # Cargar la query desde archivo usando la utilidad
        sql = DWConnectionUtils.sql_load('warehouse', 'listar_colaboradores.sql')
        params = []
        if ver_planta:
            sql = sql.replace('--filter--', " AND centro_costo  in %s")            
            params=[tuple(centro_costo)]
        else:
            sql = sql.replace('--filter--', " AND centro_costo  in (%s) AND planta_noplanta='NP'")
            params=[tuple(centro_costo)]
            ##print(sql)
        return DWConnectionUtils.fetch_dicts(sql, params)
    
    @staticmethod
    def buscar_colaborador_por_correo(correo_flesan):
        """
        Busca un colaborador específico por su correo electrónico.
        Retorna un dict con los datos del colaborador o None si no se encuentra.
        """
        # Cargar la query desde archivo usando la utilidad
        sql = DWConnectionUtils.sql_load('warehouse', 'buscar_colaborador_por_correo.sql')
        # Usar la utilidad general para ejecutar la consulta y obtener los resultados
        result = DWConnectionUtils.fetch_dicts(sql, [correo_flesan])
        return result[0] if result else None
    
    @staticmethod
    def external_code_162():
        # Cargar la query desde archivo usando la utilidad
        sql = DWConnectionUtils.sql_load('warehouse', 'external_code_162.sql')
        # Usar la utilidad general para ejecutar la consulta y obtener los resultados
        return DWConnectionUtils.fetch_dicts(sql)
    
    @staticmethod
    def obtener_compensacion_por_np(np):
        """
        Obtiene el sueldo base y valor de hora extra de un colaborador por su NP.
        Retorna un dict con np, sueldo_base y valor_hr_extras o None si no se encuentra.
        """
        # Cargar la query desde archivo usando la utilidad
        sql = DWConnectionUtils.sql_load('warehouse', 'obtener_compensacion_por_np.sql')
        # Usar la utilidad general para ejecutar la consulta y obtener los resultados
        result = DWConnectionUtils.fetch_dicts(sql, [np])
        return result[0] if result else None