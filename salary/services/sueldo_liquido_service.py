from salary.services.afp_service import calculo_descuento_afp,seguro_cesantia
from salary.services.impuesto_service import impuesto_unico_sii
from salary.services.salud_service import calculo_descuento_salud
from warehouse.repositories.uf_repository import UfRepository
from datetime import datetime, timedelta

INGRESO_MINIMO_MENSUAL = 529000

def calculo_sueldo_liquido(
    sueldo_base: float,
    tipo_contrato: int,
    afp: str,
    salud: str='Fonasa',
    gratificacion: float=0,
    asignacion_familiar: float=0,
    asignacion_colacion: float=0,
    asignacion_transporte: float=0,
    asignacion_otros: float=0):
    #Calculo de sueldo imponible
    sueldo_imponible = sueldo_base + gratificacion 
    #descuentos AFP, Salud y AFC
    descuento_afp = calculo_descuento_afp(sueldo_imponible, afp)
    descuento_salud = calculo_descuento_salud(sueldo_imponible,salud)
    descuento_cesantia_dict = seguro_cesantia(sueldo_imponible, tipo_contrato)
    descuento_cesantia = descuento_cesantia_dict['aporte_trabajador']
    
    #Sueldo Tributario
    sueldo_tributario = sueldo_imponible - descuento_afp - descuento_salud - descuento_cesantia+asignacion_familiar+asignacion_colacion+asignacion_transporte+asignacion_otros
    #Indicadores
    today = datetime.now()  
    indicadores = UfRepository.get_utm_uf_by_date(today)
    #Impuesto
    impuesto = impuesto_unico_sii(sueldo_tributario, indicadores['valor_utm'])
    #Resumen
    haberes = sueldo_base+gratificacion + asignacion_familiar + asignacion_colacion + asignacion_transporte + asignacion_otros
    deberes = descuento_afp + descuento_salud + descuento_cesantia + impuesto
    sueldo_liquido = haberes - deberes

    data={
        "haberes": {
            "sueldo_base": sueldo_base,
            "gratificacion": gratificacion,
            "asignacion_familiar": asignacion_familiar,
            "asignacion_colacion": asignacion_colacion,
            "asignacion_transporte": asignacion_transporte,
            "asignacion_otros": asignacion_otros,
            "Total haberes": haberes
        },
        "deberes": {
            "descuento_afp": descuento_afp,
            "descuento_salud": descuento_salud,
            "descuento_cesantia": descuento_cesantia,
            "impuesto": impuesto,
            "Total descuentos": deberes
        },
        "sueldo_liquido": sueldo_liquido,
        "indicadores": indicadores
    }
    print("data",data)
    return data

def calcular_gratificacion(sueldo_base: float, ingreso_minimo_mensual: float, monto_manual: float = None) -> dict:
    """
    Calcula la gratificación legal (anual y mensual) o usa un monto arbitrario si se entrega.
    
    :param sueldo_base: Sueldo mensual imponible del trabajador.
    :param ingreso_minimo_mensual: Valor vigente del Ingreso Mínimo Mensual.
    :param monto_manual: Si se entrega, este reemplaza al cálculo legal.
    :return: dict con detalle de cálculo.
    """
    
    # Gratificación legal anual (25% con tope 4,75 IMM)
    gratificacion_legal = sueldo_base * 0.25
    tope_gratificacion = ingreso_minimo_mensual * 4.75
    gratificacion_legal = min(gratificacion_legal, tope_gratificacion)
    
    # Si el usuario entrega un monto manual, se usa ese
    if monto_manual is not None:
        gratificacion_final = max(gratificacion_legal, monto_manual)
        origen = "Monto manual ingresado"
    else:
        gratificacion_final = gratificacion_legal
        origen = "Cálculo legal"
    
    return {
        "sueldo_base": sueldo_base,
        "ingreso_minimo_mensual": ingreso_minimo_mensual,
        "gratificacion_legal": round(gratificacion_legal, 2),
        "gratificacion_final": round(gratificacion_final, 2),
        "origen": origen
    }


def calculo_sueldo_bruto_desde_liquido(
    sueldo_liquido_deseado: float,
    tipo_contrato: int,
    afp: str,
    salud: str='Fonasa',
    gratificacion: bool=False,
    asignacion_familiar: float=0,
    asignacion_colacion: float=0,
    asignacion_transporte: float=0,
    asignacion_otros: float=0,
    tolerancia: float=100.0,
    max_iteraciones: int=100):
    """
    Calcula el sueldo base necesario para obtener un sueldo líquido específico mediante iteración.
    
    Args:
        sueldo_liquido_deseado: Sueldo líquido objetivo
        tipo_contrato: Tipo de contrato del colaborador
        afp: AFP del colaborador
        salud: Sistema de salud (default: 'Fonasa')
        gratificacion: Monto de gratificación (default: 0)
        asignacion_familiar: Monto de asignación familiar (default: 0)
        asignacion_colacion: Monto de asignación de colación (default: 0)
        asignacion_transporte: Monto de asignación de transporte (default: 0)
        asignacion_otros: Otros montos de asignaciones (default: 0)
        tolerancia: Diferencia máxima aceptable entre sueldo líquido calculado y deseado (default: 100.0)
        max_iteraciones: Número máximo de iteraciones (default: 100)
    
    Returns:
        dict: Resultado del cálculo con el sueldo base encontrado y detalles del cálculo
    """
    
    # Estimación inicial: sueldo base = sueldo líquido * 1.25
    sueldo_base_estimado = sueldo_liquido_deseado * 1.25
    
    # Variables para el algoritmo iterativo
    iteracion = 0
    diferencia = float('inf')
    factor_ajuste = 0.1  # Factor para ajustar el sueldo base en cada iteración
    
    # Historial para evitar oscilaciones
    historial_diferencias = []
    mejor_sueldo_base = sueldo_base_estimado
    menor_diferencia = float('inf')
    
    while abs(diferencia) > tolerancia and iteracion < max_iteraciones:
        iteracion += 1
        
        try:
            #Calcular gratificacion
            if gratificacion:
                resultado_gratificacion = calcular_gratificacion(sueldo_base_estimado, INGRESO_MINIMO_MENSUAL)
                monto_gratificacion = resultado_gratificacion['gratificacion_final']
            else:
                monto_gratificacion = 0
            # Calcular sueldo líquido con el sueldo base estimado actual
            resultado_calculo = calculo_sueldo_liquido(
                sueldo_base=sueldo_base_estimado,
                tipo_contrato=tipo_contrato,
                afp=afp,
                salud=salud,
                gratificacion=monto_gratificacion,
                asignacion_familiar=asignacion_familiar,
                asignacion_colacion=asignacion_colacion,
                asignacion_transporte=asignacion_transporte,
                asignacion_otros=asignacion_otros
            )
            
            sueldo_liquido_calculado = resultado_calculo['sueldo_liquido']
            diferencia = sueldo_liquido_deseado - sueldo_liquido_calculado
            
            # Guardar el mejor resultado hasta ahora
            if abs(diferencia) < menor_diferencia:
                menor_diferencia = abs(diferencia)
                mejor_sueldo_base = sueldo_base_estimado
            
            # Agregar al historial
            historial_diferencias.append(diferencia)
            
            # Si estamos muy cerca, salir del bucle
            if abs(diferencia) <= tolerancia:
                break
            
            # Ajustar el sueldo base para la siguiente iteración
            # Si el sueldo líquido calculado es menor al deseado, necesitamos aumentar el sueldo base
            if diferencia > 0:
                # Necesitamos más sueldo líquido, aumentar sueldo base
                ajuste = abs(diferencia) * (1 + factor_ajuste)
            else:
                # Tenemos demasiado sueldo líquido, reducir sueldo base
                ajuste = abs(diferencia) * (1 + factor_ajuste)
                ajuste = -ajuste
            
            sueldo_base_estimado += ajuste
            
            # Evitar sueldos base negativos
            if sueldo_base_estimado < 0:
                sueldo_base_estimado = sueldo_liquido_deseado * 0.5
            
            # Detectar oscilaciones y ajustar factor
            if len(historial_diferencias) >= 3:
                # Si las últimas 3 diferencias cambian de signo, reducir factor de ajuste
                ultimas_3 = historial_diferencias[-3:]
                if (ultimas_3[0] > 0 and ultimas_3[1] < 0 and ultimas_3[2] > 0) or \
                   (ultimas_3[0] < 0 and ultimas_3[1] > 0 and ultimas_3[2] < 0):
                    factor_ajuste *= 0.5
                    factor_ajuste = max(factor_ajuste, 0.01)  # Mínimo factor
            
        except Exception as e:
            # Si hay error en el cálculo, usar el mejor resultado hasta ahora
            print("Error en el cálculo: ", e)
            sueldo_base_estimado = mejor_sueldo_base
            break
    
    # Calcular el resultado final con el mejor sueldo base encontrado
    resultado_final = calculo_sueldo_liquido(
        sueldo_base=mejor_sueldo_base,
        tipo_contrato=tipo_contrato,
        afp=afp,
        salud=salud,
        gratificacion=monto_gratificacion,
        asignacion_familiar=asignacion_familiar,
        asignacion_colacion=asignacion_colacion,
        asignacion_transporte=asignacion_transporte,
        asignacion_otros=asignacion_otros
    )
    
    # Agregar información del proceso iterativo
    resultado_final['calculo_inverso'] = {
        'sueldo_liquido_deseado': sueldo_liquido_deseado,
        'sueldo_liquido_obtenido': resultado_final['sueldo_liquido'],
        'diferencia_final': resultado_final['sueldo_liquido'] - sueldo_liquido_deseado,
        'iteraciones_realizadas': iteracion,
        'convergencia_exitosa': abs(resultado_final['sueldo_liquido'] - sueldo_liquido_deseado) <= tolerancia,
        'tolerancia_utilizada': tolerancia,
        'sueldo_base_calculado': mejor_sueldo_base
    }
    
    return resultado_final