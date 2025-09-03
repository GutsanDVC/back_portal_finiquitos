import os
import psycopg2
from dotenv import load_dotenv
from utils.txt_logger import writeTxtLog
# Repositorio para acceso directo a la tabla portal_finiquitos.global_access_user
# Todas las operaciones se hacen por SQL directo, no ORM.

# Helper de conexión a PostgreSQL usando variables de entorno
load_dotenv()  # Cargar variables desde .env

def get_db_connection():
    """Obtiene una conexión psycopg2 usando variables de entorno.
    Requiere: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
    """
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', '5432')
    print(db_name)
    print(db_user)
    print(db_password)
    print(db_host)
    print(db_port)
    if not all([db_name, db_user, db_password, db_host, db_port]):
        raise RuntimeError('Faltan variables de entorno de base de datos (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT).')
    return psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)

# CREATE

def crear_usuario_global(np, nombre, email, usuario_creo,activo,ver_nfg):
    """
    Inserta un nuevo usuario global en la tabla existente usando SQL directo.
    """
    email=email.lower() # Convertir a minúsculas para hacer la búsqueda insensible a mayúsculas y minúsculas
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO portal_finiquitos.global_access_user (np, nombre, email, usuario_creo, created_at,activo,ver_nfg)
                VALUES (%s, %s, %s, %s, NOW(),%s,%s)
            """, [np, nombre, email, usuario_creo,activo,ver_nfg])
        conn.commit()

# READ

def obtener_usuarios_globales():
    """
    Obtiene todos los usuarios globales usando SQL directo.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT np, nombre, email, usuario_creo, created_at,activo,ver_nfg
                FROM portal_finiquitos.global_access_user
                --WHERE activo = true
            """)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

def obtener_usuario_por_np(np):
    """
    Obtiene un usuario global por su número personal (np).
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT np, nombre, email, usuario_creo, created_at, activo, ver_nfg
                FROM portal_finiquitos.global_access_user
                WHERE np = %s AND activo = true
            """, [np])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

def obtener_usuario_por_email(email):
    """
    Obtiene un usuario global por su email.
    """
    email=email.lower() # Convertir a minúsculas para hacer la búsqueda insensible a mayúsculas y minúsculas
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            writeTxtLog("email",email,"INFO")
            cursor.execute("""
                SELECT np, nombre, email, usuario_creo, created_at, activo, ver_nfg
                FROM portal_finiquitos.global_access_user
                WHERE email = %s AND activo = true
            """, [email])
            row = cursor.fetchone()
            writeTxtLog("row",row,"INFO")
            if row:
                columns = [col[0] for col in cursor.description]
                response = dict(zip(columns, row))
                writeTxtLog("response",response,"INFO")
                return response
            return None

# UPDATE

def actualizar_usuario_global(np, nombre=None, email=None, usuario_creo=None, activo=None, ver_nfg=None):
    """
    Actualiza los datos de un usuario global identificado por su np.
    Solo actualiza los campos que se pasan como argumento.
    """
    campos = []
    valores = []
    if nombre is not None:
        campos.append('nombre = %s')
        valores.append(nombre)
    if email is not None:
        campos.append('email = %s')
        valores.append(email)
    if usuario_creo is not None:
        campos.append('usuario_creo = %s')
        valores.append(usuario_creo)
    if activo is not None:
        campos.append('activo = %s')
        valores.append(activo)
    if ver_nfg is not None:
        campos.append('ver_nfg = %s')
        valores.append(ver_nfg)
    if not campos:
        return False  # Nada que actualizar
    valores.append(np)
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                UPDATE portal_finiquitos.global_access_user
                SET {', '.join(campos)}
                WHERE np = %s
            """, valores)
        conn.commit()
        return True

# DELETE

def eliminar_usuario_global(np):
    """
    Elimina un usuario global por su número personal (np).
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM portal_finiquitos.global_access_user WHERE np = %s
            """, [np])
        conn.commit()
        return True

def existe_email_o_np(email, np):
    """
    Verifica si ya existe un usuario con el mismo email o np.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM portal_finiquitos.global_access_user WHERE email = %s OR np = %s
            """, [email, np])
            return cursor.fetchone()[0] > 0

# --- Fin CRUD ---
