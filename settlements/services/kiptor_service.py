import os
import requests

KIPTOR_USER ='flesan-kiptor' #os.getenv("KIPTOR_USER")
KIPTOR_PASS = os.getenv("KIPTOR_PASS")

def get_kiptor_token():
    """
    Obtiene el token de autenticación desde la API de Kiptor.
    """
    url = "https://node.kiptor.com/autenticar"
    body = {
        "usuario": KIPTOR_USER,
        "contrasena": KIPTOR_PASS
    }
    response = requests.post(url, json=body, headers={"Content-Type": "application/json"},verify=False)
    if response.status_code == 200:
        return response.json().get("token")
    raise Exception(f"Error al autenticar en Kiptor: {response.status_code} - {response.text}")

from datetime import date, datetime

def serialize_dates(obj):
    """
    Convierte todos los objetos date/datetime de un dict/list anidados a string ISO.
    """
    if isinstance(obj, dict):
        return {k: serialize_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_dates(item) for item in obj]
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    else:
        return obj

def simulate_settlement_kiptor(data):
    """
    Simula el finiquito usando la API de Kiptor.
    """
    token = get_kiptor_token()
    url = "https://node.kiptor.com/simuladores/finiquitos"
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    data_serialized = serialize_dates(data)
    print(data_serialized)
    response = requests.post(url, json=data_serialized, headers=headers,verify=False)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error al simular finiquito: {response.status_code} - {response.text}")
