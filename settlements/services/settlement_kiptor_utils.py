from datetime import datetime

class FiniquitoRequestData:
    """
    Clase para estructurar el payload exactamente como lo requiere la API de Kiptor,
    con las propiedades y formato del ejemplo proporcionado.
    """
    def __init__(self, data):
        self.finiquito = {
            "carta_aviso": data["finiquito"].get("carta_aviso", 0),
            "isap": data["finiquito"].get("isap", 1),
            "tope_indemnizaciones": data["finiquito"].get("tope_indemnizaciones", 1),
            "valor_uf": data["finiquito"].get("valor_uf", 37000),
            "tope_anios": data["finiquito"].get("tope_anios", 1),
            "fecha_ingreso": data["finiquito"].get("fecha_ingreso", ""),
            "fecha_termino": data["finiquito"].get("fecha_termino", ""),
            "fecha_ultimo_imposiciones": data["finiquito"].get("fecha_ultimo_imposiciones", ""),
            "fecha_proximo_imposiciones": data["finiquito"].get("fecha_proximo_imposiciones", ""),
            "causal_derecho": data["finiquito"].get("causal_derecho", ""),
            "letra": data["finiquito"].get("letra", ""),
            "causal_hecho": data["finiquito"].get("causal_hecho", "")
        }
        self.conceptos = {
            "imp": data["conceptos"].get("imp", {}),
            "nimp": data["conceptos"].get("nimp", {}),
            "adicionales": data["conceptos"].get("adicionales", {}),
            "descuentos": data["conceptos"].get("descuentos", {})
        }
        self.vacaciones = {
            "factor_diario": data["vacaciones"].get("factor_diario", 0),
            "saldo_en_dias": data["vacaciones"].get("saldo_en_dias", 0),
            "fecha_saldo": data["vacaciones"].get("fecha_saldo", "")
        }

    def __str__(self):
        return str({
            "finiquito": self.finiquito,
            "conceptos": self.conceptos,
            "vacaciones": self.vacaciones
        })


def parsear_datos(request_data):
    """
    Extrae y transforma los datos de la request para el cálculo de finiquito y simulación.
    """
    return {
        "centro_costo": request_data.get("centro_costo"),
        "correo_flesan": request_data.get("correo_flesan"),
        "correo_gmail": request_data.get("correo_gmail"),
        "empl_status": request_data.get("empl_status"),
        "empresa": request_data.get("empresa"),
        "external_cod_cargo": request_data.get("external_cod_cargo"),
        "external_cod_tipo_contrato": request_data.get("external_cod_tipo_contrato"),
        "fecha_fin_contrato": request_data.get("fecha_fin_contrato"),
        "fecha_ingreso_date": request_data.get("fecha_ingreso_date"),
        "fecha_termino": request_data.get("fecha_termino"),
        "first_name": request_data.get("first_name"),
        "last_name": request_data.get("last_name"),
        "national_id": request_data.get("national_id"),
        "np": str(request_data.get("user_id")),
        "nombre_centro_costo": request_data.get("nombre_centro_costo"),
        # Formulario anidado
        "causalTermino": request_data.get("form", {}).get("causalTermino"),
        "descuentoAfc": request_data.get("form", {}).get("descuentoAfc"),
        "fecha_desvinculacion": request_data.get("form", {}).get("fecha_desvinculacion"),
        "grat": request_data.get("form", {}).get("grat"),
        "tipo_solicitud": request_data.get("form", {}).get("tipo_solicitud"),
    }

def parsear_resultado(resultado):
    """
    Extrae y transforma el resultado de SettlementRepository.calcular_finiquito.
    """
    datos = {
         "fecha_ingreso": resultado[0]['fecha_ingreso'],
         "factor_diario": round(float(resultado[0]['ponderacion']),5),
         "saldo_en_dias": round(float(resultado[0]['ponderacion_vacaciones']),5),
         "fecha_saldo":  resultado[0]['fecha_vacacion']
    }
    for res in resultado:
        if res['tipo_2'] == 'variable' and res['tipo'] == 'imponible':
            datos['variable_im'] = res['importe']
        if res['tipo_2'] == 'variable' and res['tipo'] == 'no imponible':
            datos['variable_ni'] = res['importe']
        else:
            datos[res['tipo_2']] = res['importe']

    return datos
    

from datetime import date, datetime

def to_yyyy_mm_dd(value):
    """
    Convierte un valor date/datetime o string ISO a 'YYYY-MM-DD' (solo fecha).
    """
    if isinstance(value, (date, datetime)):
        return value.strftime('%Y-%m-%d')
    if isinstance(value, str):
        # Si ya está bien, lo deja, si tiene T o espacio, lo corta
        return value.split('T')[0].split(' ')[0]
    return value

def parsear_body_for_kiptor(data_colaborador,datos_finiquito,valor_uf):
    finiquito = {
            "carta_aviso": 0,
            "isap": int(data_colaborador['mes_aviso']),
            "tope_indemnizaciones": 1,
            "valor_uf": int(valor_uf),
            "tope_anios": 1,
            "fecha_ingreso": to_yyyy_mm_dd(datos_finiquito['fecha_ingreso']),
            "fecha_termino": to_yyyy_mm_dd(data_colaborador['fecha_desvinculacion']),
            "fecha_ultimo_imposiciones": "",
            "fecha_proximo_imposiciones": "",
            "causal_derecho": data_colaborador['causalTermino'],
            "letra":"\\N" ,
            "causal_hecho": ""
        }
    vacaciones = {
            "factor_diario": round(float(datos_finiquito['factor_diario']),5),
            "saldo_en_dias": round(float(datos_finiquito['saldo_en_dias']),5),
            "fecha_saldo":  datos_finiquito['fecha_saldo']
        }
    conceptos = {
            "imp": {
                "sueldo_base":datos_finiquito['BASE'],
                
            },
            "nimp": {},
        }
    # Usar .get() para evitar KeyError y permitir valores opcionales
    if datos_finiquito.get('GRATIFICACION'):
        conceptos['imp']['gratificacion'] = datos_finiquito['GRATIFICACION']
    if datos_finiquito.get('VARIABLE_IM'):
        conceptos['imp']['variable'] = datos_finiquito['VARIABLE_IM']
    if datos_finiquito.get('VARIABLE_NI'):
        conceptos['nimp']['variable'] = datos_finiquito['VARIABLE_NI']
    if datos_finiquito.get('MOVILIZACION'):
        conceptos['nimp']['movilizacion'] = datos_finiquito['MOVILIZACION']
    if datos_finiquito.get('COLACION'):
        conceptos['nimp']['colacion'] = datos_finiquito['COLACION']
    if datos_finiquito.get('INDEMNIZACION'):
        conceptos['adicionales']['indemnizacion'] = datos_finiquito['INDEMNIZACION']
    if datos_finiquito.get('DESCUENTO'):
        conceptos['descuentos']['descuento'] = datos_finiquito['DESCUENTO']
    
    return {
        "finiquito": finiquito,
        "conceptos": conceptos,
        "vacaciones": vacaciones
    }

def parsear_todo(request_data, resultado_finiquito, resultado_kiptor):
    """
    Junta y ordena los datos para la respuesta final.
    """
    body = resultado_kiptor.get("body", {})
    indemnizaciones = body.get("indemnizaciones", {})
    return {
        "np": resultado_finiquito.get("np"),
        "anios_servicio": resultado_finiquito.get("anios_servicio"),
        "tiempo_servido": resultado_finiquito.get("tiempo_servido"),
        "saldo_en_dias": resultado_finiquito.get("saldo_en_dias"),
        "dias_inhabiles": resultado_finiquito.get("dias_inhabiles"),
        "total_dias": resultado_finiquito.get("total_dias"),
        "base_indemnizaciones": body.get("Bases", {}).get("base_indemnizaciones"),
        "base_vacaciones": body.get("Bases", {}).get("base_vacaciones"),
        "ias": indemnizaciones.get("IAS"),
        "isap": indemnizaciones.get("ISAP"),
        "its": indemnizaciones.get("ITS"),
        "ivac": indemnizaciones.get("IVAC"),
        "total_finiquito": body.get("total_finiquito"),
        "fecha_desvinculacion": request_data.get("form", {}).get("fecha_desvinculacion"),
        "causal": request_data.get("form", {}).get("causalTermino"),
        "letra_causal": get_letra_causal(request_data.get("form", {}).get("causalTermino")),
        "fecha_inset": resultado_finiquito.get("fecha_inset"),
        "national_id": request_data.get("national_id"),
        "first_name": request_data.get("first_name"),
        "last_name": request_data.get("last_name"),
    }



def get_letra_causal(causal):
    """
    Devuelve la letra de la causal, por ejemplo para '161-1' retorna 'a'.
    """
    if causal and '-' in causal:
        try:
            return chr(96 + int(causal.split('-')[1]))  # 1 -> 'a', 2 -> 'b', etc.
        except Exception:
            return ""
    return ""
