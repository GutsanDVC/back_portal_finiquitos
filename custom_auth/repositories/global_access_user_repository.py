from django.db import connection

# Repositorio para acceso directo a la tabla portal_finiquitos.global_access_user
# Todas las operaciones se hacen por SQL directo, no ORM.

# CREATE

def crear_usuario_global(np, nombre, email, usuario_creo):
    """
    Inserta un nuevo usuario global en la tabla existente usando SQL directo.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO portal_finiquitos.global_access_user (np, nombre, email, usuario_creo, created_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, [np, nombre, email, usuario_creo])

# READ

def obtener_usuarios_globales():
    """
    Obtiene todos los usuarios globales usando SQL directo.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT np, nombre, email, usuario_creo, created_at
            FROM portal_finiquitos.global_access_user
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def obtener_usuario_por_np(np):
    """
    Obtiene un usuario global por su número personal (np).
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT np, nombre, email, usuario_creo, created_at
            FROM portal_finiquitos.global_access_user
            WHERE np = %s
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
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT np, nombre, email, usuario_creo, created_at
            FROM portal_finiquitos.global_access_user
            WHERE email = %s
        """, [email])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        return None

# UPDATE

def actualizar_usuario_global(np, nombre=None, email=None, usuario_creo=None):
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
    if not campos:
        return False  # Nada que actualizar
    valores.append(np)
    with connection.cursor() as cursor:
        cursor.execute(f"""
            UPDATE portal_finiquitos.global_access_user
            SET {', '.join(campos)}
            WHERE np = %s
        """, valores)
        return cursor.rowcount > 0

# DELETE

def eliminar_usuario_global(np):
    """
    Elimina un usuario global por su número personal (np).
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM portal_finiquitos.global_access_user WHERE np = %s
        """, [np])
        return cursor.rowcount > 0

def existe_email_o_np(email, np):
    """
    Verifica si ya existe un usuario con el mismo email o np.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM portal_finiquitos.global_access_user WHERE email = %s OR np = %s
        """, [email, np])
        return cursor.fetchone()[0] > 0

# --- Fin CRUD ---
