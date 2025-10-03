with centros_costos as(
SELECT 
	distinct centro_costo
	,empresa
FROM flesan_rrhh.sap_maestro_colaborador AS smc
WHERE 
    empl_status='41111'
order by empresa,centro_costo
),
empresas as (
SELECT mr.* FROM public.maestro_rut AS mr
where not rut in (
'76418768-7',
'76780803-8',
'76230125-3',
'76879359-K',
'76948230-K',
'77287778-1',
'77902252-8',
'76675510-0',
'76259020-4',
'76259040-9',
'76474409-8',
'76543353-3',
'76710873-7',
'78086195-9',
'77092703-K'
))
select centros_costos.*from centros_costos join
empresas
on centros_costos.empresa=empresas.id_sap