from django.conf import settings
from django.core.exceptions import ValidationError
import requests
import os

def google_validate_id_token(*, id_token: str) -> dict:

    response = requests.get(
        settings.GOOGLE_ID_TOKEN_INFO_URL, params={"id_token": id_token}
    )
    if not response.ok:
        raise ValidationError("id_token is invalid.")

    token_info = response.json()

    audience = token_info["aud"]

    # Prints de depuración
    print("audience recibido:", audience)
    print("GOOGLE_AUTH_CLIENT_ID (os.getenv):", os.getenv("GOOGLE_AUTH_CLIENT_ID"))
    print("GOOGLE_AUTH_CLIENT_ID (settings):", getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID", None))

    if audience != os.getenv("GOOGLE_AUTH_CLIENT_ID"):
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


def parsear_admin_access(admin_access: list,user_data: dict) -> dict:
    data={
        "email":user_data.get("email"),
        "name":user_data.get("name"),
        "admin_access":[]
    }
    if not admin_access:
        return data
    data['admin_access'] = admin_access
    return data

def parsear_global_access(global_access: list,user_data: dict) -> dict:
    data={
        "email":user_data.get("email"),
        "name":user_data.get("name"),
        "admin_access":[]
    }
    listar_centros_costo = CentroCostoRepository.listar_centros_costo()
    access=[
        {
            "centro_costo":centro_costo,
            "label":centro_costo.get("label"),
            "name":centro_costo.get("name")
        }
        for centro_costo in listar_centros_costo
    ]
    data['admin_access'] = access
    return data
        