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
    
    @staticmethod
    def get_utm_uf_by_date(fecha):
        """
        Retorna el valor de la UTM y UF más reciente anterior o igual al mes de la fecha dada.
        :param fecha: Fecha en formato string (YYYY-MM-DD)
        :return: dict con valor_utm y fecha | valor_uf | dolar
        """
        sql = DWConnectionUtils.sql_load('warehouse', 'get_utm_uf_by_date.sql')
        params = {'fecha': fecha}
        with DWConnectionUtils.get_dw_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                row = cursor.fetchone()
                #(datetime.date(2025, 8, 31), '39383.07', '68647', '967.48')
                if row:
                    return {'fecha': row[0], 'valor_utm': row[2], 'valor_uf': row[1], 'dolar': row[3]}
                return None
    