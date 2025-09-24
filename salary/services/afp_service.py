import requests
import re
import datetime as dt
from bs4 import BeautifulSoup
from decimal import Decimal

# URL oficial donde publican las comisiones vigentes
URL = "https://www.spensiones.cl/portal/institucional/594/w3-article-2815.html"

MONTHS_ES = {
    "enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,
    "julio":7,"agosto":8,"septiembre":9,"setiembre":9,"octubre":10,
    "noviembre":11,"diciembre":12
}
AFP={
    "CAPITAL": "Capital",
    "CUPRUM": "Cuprum",
    "HABITAT": "Habitat",
    "MODEL": "Modelo",
    "PLANVITAL": "Planvital",
    "PROVIDA": "Provida",
    "UNO": "Uno"
}

def get_afp_commissions():
    r = requests.get(URL, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    html_text = soup.get_text(" ", strip=True)

    # Busca "Septiembre 2025" o similar en el texto para fijar el período
    m = re.search(r'(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre)\s+(\d{4})',
                  html_text, flags=re.I)
    if m:
        mes = MONTHS_ES[m.group(1).lower()]
        year = int(m.group(2))
        periodo = dt.date(year, mes, 1).isoformat()
    else:
        # fallback: mes actual
        today = dt.date.today()
        periodo = dt.date(today.year, today.month, 1).isoformat()

    # Extrae las AFP y sus porcentajes
    patt = re.compile(r'AFP\s+([A-Za-zÁÉÍÓÚÜÑñ]+)\s*:\s*([\d.,]+)\s*%', re.I)
    data = {}
    for name, pct in patt.findall(html_text):
        pct_decimal = Decimal(pct.replace('.', '').replace(',', '.'))
        data[name.title()] = float(pct_decimal)

    return {"periodo": periodo, "fuente": URL, "comisiones": data}

def calculo_descuento_afp(monto_imponible_clp: float,afp: str):
    resultado = get_afp_commissions()
    monto_afp = monto_imponible_clp * (resultado["comisiones"][afp]+10) / 100    
    return monto_afp

def seguro_cesantia(sueldo_imponible: float, tipo_contrato: int) -> dict:
    """
    Calcula el Seguro de Cesantía en Chile.

    :param sueldo_imponible: Monto imponible sobre el cual se calculan las cotizaciones.
    :param tipo_contrato: 1 = contrato indefinido, 0 = plazo fijo/obra.
    :return: Diccionario con aporte trabajador, aporte empresa y descuento total.
    """
    # Tope imponible en UF (se actualiza periódicamente)
    TOPE_UF = 122.6
    VALOR_UF = 37000  # <- aquí debes poner el valor vigente de la UF en pesos
    TOPE_IMPONIBLE = TOPE_UF * VALOR_UF

    # Aplicar tope imponible
    base_calculo = min(sueldo_imponible, TOPE_IMPONIBLE)

    if tipo_contrato == 1:  # Contrato indefinido
        aporte_trabajador = base_calculo * 0.006   # 0,6%
        aporte_empresa = base_calculo * 0.024      # 2,4%
    else:  # Contrato plazo fijo / obra
        aporte_trabajador = 0.0
        aporte_empresa = base_calculo * 0.03       # 3%

    return {
        "aporte_trabajador": round(aporte_trabajador, 2),
        "aporte_empresa": round(aporte_empresa, 2),
        "descuento_total": round(aporte_trabajador + aporte_empresa, 2)
    }
