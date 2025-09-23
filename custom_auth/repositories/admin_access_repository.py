from utils.dw_utils import DWConnectionUtils
from utils.txt_logger import writeTxtLog
class AdminAccessRepository:
    @staticmethod
    def get_admin_access_by_email(email: str):
        sql = DWConnectionUtils.sql_load('custom_auth', 'get_admin_access.sql')
        try:
            with DWConnectionUtils.get_dw_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {'correo': email})
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    if not rows:
                        return []
                    result = [dict(zip(columns, row)) for row in rows]
            return result
        except Exception as e:
            writeTxtLog(str(e),"ERROR")
            return []
