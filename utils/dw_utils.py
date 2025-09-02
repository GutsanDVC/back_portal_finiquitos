import psycopg2
import os

class DWConnectionUtils:
    """
    Utilidad general para obtener una conexión al Data Warehouse (DW).
    Utiliza variables de entorno para los parámetros de conexión.
    """
    @staticmethod
    def get_dw_connection():
        """
        Retorna una conexión psycopg2 al DW usando variables de entorno.
        """
        print(os.getenv('DB_NAME_DW'))
        print(os.getenv('DB_USER_DW'))
        print(os.getenv('DB_PASSWORD_DW'))
        print(os.getenv('DB_HOST_DW'))
        print(os.getenv('DB_PORT_DW'))
        
        return psycopg2.connect(
            dbname=os.getenv('DB_NAME_DW'),
            user=os.getenv('DB_USER_DW'),
            password=os.getenv('DB_PASSWORD_DW'),
            host=os.getenv('DB_HOST_DW'),
            port=os.getenv('DB_PORT_DW')
        )

    @staticmethod
    def sql_load(modulo: str, archivo: str) -> str:
        """
        Carga el contenido de un archivo SQL ubicado en <modulo>/repositories/sql/<archivo>.
        Args:
            modulo: Nombre del módulo (ej: 'warehouse').
            archivo: Nombre del archivo SQL (ej: 'listar_colaboradores.sql').
        Returns:
            Contenido del archivo SQL como string.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sql_path = os.path.join(base_dir, modulo, 'repositories', 'sql', archivo)
        with open(sql_path, encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def fetch_dicts(sql: str, params=None) -> list:
        """
        Ejecuta una consulta SQL y retorna los resultados como lista de diccionarios.
        Args:
            sql: Consulta SQL a ejecutar.
            params: Parámetros opcionales para la consulta.
        Returns:
            Lista de diccionarios con los resultados.
        """
        results = []
        with DWConnectionUtils.get_dw_connection() as conn:
            #print(sql) # DEBUG
            with conn.cursor() as cur:
                cur.execute(sql, params or [])
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                #print(rows) # DEBUG
                for row in rows:
                    results.append(dict(zip(columns, row)))
                #print(results) # DEBUG
        return results
