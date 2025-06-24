SELECT 
	distinct centro_costo
	,empresa
FROM flesan_rrhh.sap_maestro_colaborador AS smc
WHERE 
    empl_status='41111'
order by empresa,centro_costo;
