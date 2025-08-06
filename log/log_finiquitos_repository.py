from django.db import connection
import json
from datetime import datetime, date
from typing import Optional, List, Dict, Any

# Repository para acceso directo a la tabla portal_finiquitos.log_finiquitos
# Todas las operaciones se hacen por SQL directo, no ORM.

# HELPER FUNCTIONS

def _json_serializer(obj):
    """
    Función helper para serializar objetos datetime y date a JSON.
    
    Args:
        obj: Objeto a serializar
        
    Returns:
        str: Representación en string del objeto
        
    Raises:
        TypeError: Si el objeto no es serializable
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


# CREATE

def crear_log_finiquito(user: str, log_accion: dict) -> int:
    """
    Inserta un nuevo log de finiquito en la tabla usando SQL directo.
    
    Args:
        user (str): Usuario que realiza la acción
        log_accion (dict): Datos de la acción en formato JSON
        
    Returns:
        int: ID del log creado
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO portal_finiquitos.log_finiquitos ("user", fecha, log_accion)
            VALUES (%s, NOW(), %s)
            RETURNING id
        """, [user, json.dumps(log_accion, default=_json_serializer)])
        return cursor.fetchone()[0]


# READ

def obtener_todos_los_logs(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Obtiene todos los logs de finiquitos con paginación usando SQL directo.
    
    Args:
        limit (int): Número máximo de registros a retornar
        offset (int): Número de registros a saltar
        
    Returns:
        List[Dict]: Lista de diccionarios con los logs
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, "user", fecha, log_accion
            FROM portal_finiquitos.log_finiquitos
            ORDER BY fecha DESC
            LIMIT %s OFFSET %s
        """, [limit, offset])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def obtener_log_por_id(log_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene un log específico por su ID.
    
    Args:
        log_id (int): ID del log a buscar
        
    Returns:
        Dict or None: Diccionario con los datos del log o None si no existe
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, "user", fecha, log_accion
            FROM portal_finiquitos.log_finiquitos
            WHERE id = %s
        """, [log_id])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        return None


def obtener_logs_por_usuario(user: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Obtiene todos los logs de un usuario específico con paginación.
    
    Args:
        user (str): Usuario del cual obtener los logs
        limit (int): Número máximo de registros a retornar
        offset (int): Número de registros a saltar
        
    Returns:
        List[Dict]: Lista de diccionarios con los logs del usuario
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, "user", fecha, log_accion
            FROM portal_finiquitos.log_finiquitos
            WHERE "user" = %s
            ORDER BY fecha DESC
            LIMIT %s OFFSET %s
        """, [user, limit, offset])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def obtener_logs_por_fecha_rango(fecha_inicio: datetime, fecha_fin: datetime, 
                                limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Obtiene logs dentro de un rango de fechas con paginación.
    
    Args:
        fecha_inicio (datetime): Fecha de inicio del rango
        fecha_fin (datetime): Fecha de fin del rango
        limit (int): Número máximo de registros a retornar
        offset (int): Número de registros a saltar
        
    Returns:
        List[Dict]: Lista de diccionarios con los logs en el rango de fechas
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, "user", fecha, log_accion
            FROM portal_finiquitos.log_finiquitos
            WHERE fecha BETWEEN %s AND %s
            ORDER BY fecha DESC
            LIMIT %s OFFSET %s
        """, [fecha_inicio, fecha_fin, limit, offset])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def buscar_logs_por_accion(accion_key: str, accion_value: Any, 
                          limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Busca logs que contengan una clave específica en el campo log_accion.
    
    Args:
        accion_key (str): Clave a buscar en el JSON log_accion
        accion_value (Any): Valor a buscar para la clave especificada
        limit (int): Número máximo de registros a retornar
        offset (int): Número de registros a saltar
        
    Returns:
        List[Dict]: Lista de diccionarios con los logs que coinciden
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, "user", fecha, log_accion
            FROM portal_finiquitos.log_finiquitos
            WHERE log_accion->>%s = %s
            ORDER BY fecha DESC
            LIMIT %s OFFSET %s
        """, [accion_key, str(accion_value), limit, offset])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


# UPDATE

def actualizar_log_finiquito(log_id: int, user: str = None, log_accion: dict = None) -> bool:
    """
    Actualiza un log de finiquito existente.
    Solo actualiza los campos que se pasan como argumento.
    
    Args:
        log_id (int): ID del log a actualizar
        user (str, optional): Nuevo usuario
        log_accion (dict, optional): Nueva acción en formato JSON
        
    Returns:
        bool: True si se actualizó correctamente, False si no se encontró el registro
    """
    campos = []
    valores = []
    
    if user is not None:
        campos.append('"user" = %s')
        valores.append(user)
    
    if log_accion is not None:
        campos.append('log_accion = %s')
        valores.append(json.dumps(log_accion, default=_json_serializer))
    
    if not campos:
        return False  # Nada que actualizar
    
    valores.append(log_id)
    
    with connection.cursor() as cursor:
        cursor.execute(f"""
            UPDATE portal_finiquitos.log_finiquitos
            SET {', '.join(campos)}
            WHERE id = %s
        """, valores)
        return cursor.rowcount > 0


# DELETE

def eliminar_log_finiquito(log_id: int) -> bool:
    """
    Elimina un log de finiquito por su ID.
    
    Args:
        log_id (int): ID del log a eliminar
        
    Returns:
        bool: True si se eliminó correctamente, False si no se encontró el registro
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM portal_finiquitos.log_finiquitos 
            WHERE id = %s
        """, [log_id])
        return cursor.rowcount > 0


def eliminar_logs_por_usuario(user: str) -> int:
    """
    Elimina todos los logs de un usuario específico.
    
    Args:
        user (str): Usuario cuyos logs se eliminarán
        
    Returns:
        int: Número de registros eliminados
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM portal_finiquitos.log_finiquitos 
            WHERE "user" = %s
        """, [user])
        return cursor.rowcount


def eliminar_logs_antiguos(dias_antiguedad: int) -> int:
    """
    Elimina logs más antiguos que el número de días especificado.
    
    Args:
        dias_antiguedad (int): Número de días de antigüedad
        
    Returns:
        int: Número de registros eliminados
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM portal_finiquitos.log_finiquitos 
            WHERE fecha < NOW() - INTERVAL '%s days'
        """, [dias_antiguedad])
        return cursor.rowcount


# UTILITY FUNCTIONS

def contar_logs_total() -> int:
    """
    Cuenta el total de logs en la tabla.
    
    Returns:
        int: Número total de logs
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM portal_finiquitos.log_finiquitos
        """)
        return cursor.fetchone()[0]


def contar_logs_por_usuario(user: str) -> int:
    """
    Cuenta el total de logs de un usuario específico.
    
    Args:
        user (str): Usuario del cual contar los logs
        
    Returns:
        int: Número total de logs del usuario
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM portal_finiquitos.log_finiquitos
            WHERE user = %s
        """, [user])
        return cursor.fetchone()[0]


def obtener_usuarios_con_logs() -> List[str]:
    """
    Obtiene una lista de todos los usuarios que tienen logs registrados.
    
    Returns:
        List[str]: Lista de usuarios únicos
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT user 
            FROM portal_finiquitos.log_finiquitos
            ORDER BY user
        """)
        return [row[0] for row in cursor.fetchall()]


# --- Fin CRUD ---
