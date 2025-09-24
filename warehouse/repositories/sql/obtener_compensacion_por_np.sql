SELECT 
    np,
    valor as sueldo_base,
    valor * 0.0079645 as valor_hr_extras
FROM flesan_rrhh.sap_maestro_compensacion
WHERE cc_nomina = 'M020'
    AND np = %s
