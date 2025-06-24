from utils.dw_utils import DWConnectionUtils

class CausalTerminoRepository:
    @staticmethod
    def listar_causales_termino():
        sql = DWConnectionUtils.sql_load('warehouse', 'listar_causales_termino.sql')
        return DWConnectionUtils.fetch_dicts(sql)
