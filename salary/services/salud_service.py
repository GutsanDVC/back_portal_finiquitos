def calculo_descuento_salud(monto_imponible_clp: float,prevision:str='Fonasa'):
    if prevision == 'Fonasa':
        descuento_salud = monto_imponible_clp * 0.07 #7% de salud
    else:
        descuento_salud = monto_imponible_clp * 0.07 #Pendiente a obtener monto plan o dejar así 
    return descuento_salud