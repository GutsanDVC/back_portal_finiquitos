select
	distinct centro_costo,
	nombre_centro_costo,
	concat(centro_costo, '-', nombre_centro_costo) as label
from
	flesan_rrhh.sap_maestro_colaborador
order by
	centro_costo;
