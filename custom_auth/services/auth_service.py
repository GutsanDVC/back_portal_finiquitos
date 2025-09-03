from django.conf import settings
from django.core.exceptions import ValidationError
import requests
import os
from warehouse.repositories.centro_costo_repository import CentroCostoRepository
from custom_auth.repositories.global_access_user_repository import obtener_usuario_por_email
from utils.txt_logger import writeTxtLog
def google_validate_id_token(*, id_token: str) -> dict:

    response = requests.get(
        settings.GOOGLE_ID_TOKEN_INFO_URL, params={"id_token": id_token}
    )
    if not response.ok:
        writeTxtLog(response,"ERROR")
        raise ValidationError("id_token is invalid.")

    token_info = response.json()

    audience = token_info["aud"]

    # Prints de depuración

    if audience != os.getenv("GOOGLE_AUTH_CLIENT_ID"):
        writeTxtLog("Invalid audience.","ERROR")
        raise ValidationError("Invalid audience.")

    user_data = {
        "email": token_info.get("email"),
        "email_verified": token_info.get("email_verified"),
        "name": token_info.get("name"),
        "picture": token_info.get("picture"),
        "given_name": token_info.get("given_name"),
        "family_name": token_info.get("family_name"),
        "sub": token_info.get("sub"),
    }

    return user_data


def puede_ver_nfg(email: str) -> bool:
    """
    Verifica si un usuario tiene permisos para ver la empresa NFG.
    
    Args:
        email (str): Email del usuario a verificar
        
    Returns:
        bool: True si el usuario puede ver NFG, False en caso contrario
    """
    try:
        usuario = obtener_usuario_por_email(email)
        if usuario:
            return usuario.get('ver_nfg', False)
        return False
    except Exception:
        # En caso de error, por seguridad retornamos False
        return False


def parsear_admin_access(admin_access: list,user_data: dict) -> dict:
    data={
        "email":user_data.get("email"),
        "name":user_data.get("name"),
        "ver_nfg":puede_ver_nfg(user_data.get("email", "")),
        "admin_access":[]
    }
    if not admin_access:
        return data
    data['admin_access'] = admin_access
    return data

def parsear_global_access(user_data: dict) -> dict:
    data={
        "email":user_data.get("email"),
        "name":user_data.get("name"),
        "ver_nfg":puede_ver_nfg(user_data.get("email", "")),
        "admin_access":[]
    }
    listar_centros_costo = CentroCostoRepository.listar_centros_costo()
    access=[
        {
            "cc":centro_costo.get("centro_costo"),
            "empresa":centro_costo.get("empresa"),
            "ver_planta":True,
        }
        for centro_costo in listar_centros_costo if centro_costo.get("empresa")!='NFG' or data.get("ver_nfg")
    ]
    data['admin_access'] = access
    return data