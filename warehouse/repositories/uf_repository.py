from utils.dw_utils import DWConnectionUtils

class UfRepository:
    @staticmethod
    def get_uf_by_date(fecha):
        """
        Retorna el valor de la UF más reciente anterior o igual al mes de la fecha dada.
        :param fecha: Fecha en formato string (YYYY-MM-DD)
        :return: dict con valor_uf y fecha
        """
        sql = DWConnectionUtils.sql_load('warehouse', 'get_uf_by_date.sql')
        params = {'fecha': fecha}
        with DWConnectionUtils.get_dw_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                row = cursor.fetchone()
                if row:
                    return {'valor_uf': row[0], 'fecha': row[1]}
                return None
