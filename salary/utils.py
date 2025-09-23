def impuesto_unico_segunda_categoria(renta_tributable_clp: float, valor_utm: float) -> float:
    """
    Calcula el impuesto único de segunda categoría en CLP.
    
    Parámetros:
    renta_tributable_clp : float -> Renta tributable mensual en pesos chilenos
    valor_utm : float -> Valor de la UTM vigente
    
    Retorna:
    float -> Monto del impuesto en pesos
    """

    # Tramos en UTM: (límite superior, tasa marginal)
    tramos = [
        (13.5, 0.00),
        (30, 0.04),
        (50, 0.08),
        (70, 0.135),
        (90, 0.23),
        (120, 0.304),
        (310, 0.35),
        (float("inf"), 0.40),
    ]

    renta_utm = renta_tributable_clp / valor_utm
    impuesto_utm = 0.0
    limite_inferior = 0.0

    for limite_superior, tasa in tramos:
        if renta_utm > limite_superior:
            # se paga todo el tramo
            impuesto_utm += (limite_superior - limite_inferior) * tasa
            limite_inferior = limite_superior
        else:
            # se paga solo lo que excede en este tramo
            impuesto_utm += (renta_utm - limite_inferior) * tasa
            break

    return impuesto_utm * valor_utm
