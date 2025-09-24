def impuesto_unico_sii(renta_imponible_clp: float, valor_utm: float) -> float:
    """
    Calcula el impuesto único de segunda categoría en CLP usando tabla oficial del SII.
    
    Parámetros:
    renta_imponible_clp : float -> Renta imponible mensual en pesos chilenos
    valor_utm : float -> Valor de la UTM vigente
    
    Retorna:
    float -> Monto del impuesto en pesos
    """

    # Tabla del SII: (límite superior en UTM, tasa, rebaja en UTM)
    tabla = [
        (13.5, 0.00, 0.00),
        (30, 0.04, 0.54),
        (50, 0.08, 1.74),
        (70, 0.135, 4.49),
        (90, 0.23, 11.49),
        (120, 0.304, 18.59),
        (310, 0.35, 24.59),
        (float("inf"), 0.40, 39.09),
    ]
    #Aseguar que valores sean float
    valor_utm = float(valor_utm)
    renta_imponible_clp = float(renta_imponible_clp)
    print("UTM",valor_utm)
    print("renta_imponible_clp",renta_imponible_clp)
    renta_utm = renta_imponible_clp / valor_utm
    print("renta_utm",renta_utm)
    
    for limite, tasa, rebaja in tabla:
        if renta_utm <= limite:
            impuesto_utm = (renta_utm * tasa) - rebaja
            # si resulta negativo (tramo exento), se corrige a 0
            return max(impuesto_utm, 0) * valor_utm
