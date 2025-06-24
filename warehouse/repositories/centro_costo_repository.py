from utils.dw_utils import DWConnectionUtils

class CentroCostoRepository:
    """
    Repository para consultar centros de costo desde el DW.
    """
    @staticmethod
    def listar_centros_costo():
        """
        Retorna un listado de centros de costo únicos con su nombre y label.
        """
        sql = DWConnectionUtils.sql_load('warehouse', 'listar_centros_costo.sql')
        return DWConnectionUtils.fetch_dicts(sql)

    @staticmethod
    def listar_centros_costo_por_user(user_access):
        """
        Retorna un listado de centros de costo únicos con su nombre y label.
        """
        sql = DWConnectionUtils.sql_load('warehouse', 'listar_centros_costo_por_user.sql')
        return DWConnectionUtils.fetch_dicts(sql, params=[user_access])