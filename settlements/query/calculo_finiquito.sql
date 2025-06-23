with
BASE_LIQ as (
select
	NUMERO_DE_PERSONAL,
	CC_NOMINA,
	MARCA,
	replace(CANTIDAD, ',', '.')::DOUBLE precision as CANTIDAD,
	IMPORTE::DOUBLE precision as IMPORTE
from
	FLESAN_RRHH.SAP_LIQUIDACIONES_GRUPO_FLESAN
where
	NUMERO_DE_PERSONAL = %(np)s
),
-- CTE PARA OBTENER LA BASE DE CC_NOMINA VARIABLE
BASE_CC_NOMINA as (
select
	NUMERO_DE_PERSONAL,
	MAX(CC_NOMINA) as CC_NOMINA,
	MARCA
from
	BASE_LIQ
where
	CC_NOMINA in ('MT70', 'MT71', 'MT72', 'MT80', 'MT81', 'MT82')
group by
	NUMERO_DE_PERSONAL,
	MARCA
),
-- CTE PARA OBTENER CASOS ESPECIALES SEGÚN SOLICITUD
CONTADOR as (
select
	NUMERO_DE_PERSONAL,
	MARCA
from
	BASE_LIQ
where
	CC_NOMINA in ('/TTK', 'MT74', 'MT70', 'MT71', 'MT72', 'MT80', 'MT81', 'MT82')
		and (
('R' = 'R'
			and MARCA < TO_CHAR(%(fecha_desvinculacion)s::DATE, 'YYYY-MM'))
			or ('R' = 'S'
				and MARCA < TO_CHAR(%(fecha_desvinculacion)s::DATE - interval '1 MONTH', 'YYYY-MM'))
)
	group by
		NUMERO_DE_PERSONAL,
		MARCA
	order by
		MARCA desc
	limit 3
),
CONTADOR_1 as (
select
	COUNT(*) as CONTA,
	NUMERO_DE_PERSONAL
from
	CONTADOR
group by
	NUMERO_DE_PERSONAL
),
VARIABL as (
select
	L.NUMERO_DE_PERSONAL,
	L.MARCA,
	MAX(L.CANTIDAD) as CANTIDAD,
	C1.CONTA
from
	BASE_LIQ L
left join BASE_CC_NOMINA BCC on
	L.NUMERO_DE_PERSONAL = BCC.NUMERO_DE_PERSONAL
	and L.MARCA = BCC.MARCA
left join CONTADOR_1 C1 on
	C1.NUMERO_DE_PERSONAL = L.NUMERO_DE_PERSONAL
where
	L.CC_NOMINA in ('/TTK', 'MT74', 'MT70', 'MT71', 'MT72', 'MT80', 'MT81', 'MT82')
		and (
(%(tipo_solicitud)s = 'R'
			and L.MARCA < TO_CHAR(%(fecha_desvinculacion)s::DATE, 'YYYY-MM'))
			or (%(tipo_solicitud)s = 'S'
				and L.MARCA < TO_CHAR(%(fecha_desvinculacion)s::DATE - interval '1 MONTH', 'YYYY-MM'))
)
			and BCC.CC_NOMINA is null
		group by
			L.NUMERO_DE_PERSONAL,
			L.MARCA,
			C1.CONTA
		order by
			L.MARCA desc
		limit 3
),
NO_VARIABL as (
select
	NUMERO_DE_PERSONAL,
	MARCA,
	CANTIDAD
from
	BASE_LIQ
where
	CC_NOMINA = '/TTK'
	and MARCA < TO_CHAR(CURRENT_DATE - interval '1 MONTH', 'YYYY-MM')
order by
	MARCA desc
limit 1
),
BASE_1 as (
select
	L.NUMERO_DE_PERSONAL,
	L.IMPORTE,
	L.MARCA,
	coalesce(replace(UR.CANTIDAD::VARCHAR, ',', '.'), '0') as CANTIDAD
from
	BASE_LIQ L
left join BASE_LIQ UR on
	UR.MARCA = L.MARCA
	and UR.CC_NOMINA = '/TTK'
	and L.NUMERO_DE_PERSONAL = UR.NUMERO_DE_PERSONAL
where
	L.CC_NOMINA = 'MI11'
	and coalesce(replace(UR.CANTIDAD::VARCHAR, ',', '.'), '0')::DOUBLE precision > 0
order by
	L.MARCA desc
limit 1
),
BASE_GRATI as (
select
	L.NUMERO_DE_PERSONAL,
	'MI11' as CC_NOMINA,
	case
		when ((B1.IMPORTE / nullif(L.CANTIDAD, 0))* 30) > %(grat)s then %(grat)s
		else ROUND((B1.IMPORTE / nullif(L.CANTIDAD, 0))* 30)
	end as IMPORTE,
	'IMPONIBLE' as TIPO,
	'NO VARIABLE' as TIPO1
from
	BASE_LIQ L
left join BASE_1 B1 on
	B1.NUMERO_DE_PERSONAL = L.NUMERO_DE_PERSONAL
where
	L.CC_NOMINA = '/TTK'
order by
	L.MARCA desc
limit 1
),
FINAL_UNION as (
select
	L.NUMERO_DE_PERSONAL,
	MAX(L.CC_NOMINA) as CC_NOMINA,
	SUM(L.IMPORTE) / nullif(V.CONTA, 0) as IMPORTE,
	'IMPONIBLE' as TIPO,
	'VARIABLE' as TIPO1
from
	BASE_LIQ L
left join VARIABL V on
	L.NUMERO_DE_PERSONAL = V.NUMERO_DE_PERSONAL
	and L.MARCA = V.MARCA
where
	L.CC_NOMINA in ('1008', '1010', '1011', '1012', '1013', '1014', '1015', '1016', '1019', '1031', '1035', '1036', '1042', '1060', '1066', '1065', '1067')
		and V.NUMERO_DE_PERSONAL is not null
	group by
		L.NUMERO_DE_PERSONAL,
		V.CONTA
union all
	select
		L.NUMERO_DE_PERSONAL,
		MAX(L.CC_NOMINA) as CC_NOMINA,
		SUM(L.IMPORTE) / nullif(V.CONTA, 0) as IMPORTE,
		'NO IMPONIBLE' as TIPO,
		'VARIABLE' as TIPO1
	from
		BASE_LIQ L
	left join VARIABL V on
		L.NUMERO_DE_PERSONAL = V.NUMERO_DE_PERSONAL
		and L.MARCA = V.MARCA
	where
		L.CC_NOMINA in ('1017', '1032', '1034', '1033', '1007')
			and V.NUMERO_DE_PERSONAL is not null
		group by
			L.NUMERO_DE_PERSONAL,
			V.CONTA
	union all
		select
			C.NP::VARCHAR,
			C.CC_NOMINA,
			C.VALOR as IMPORTE,
			'IMPONIBLE' as TIPO,
			'NO VARIABLE' as TIPO1
		from
			FLESAN_RRHH.SAP_MAESTRO_COMPENSACION C
		where
			C.NP = %(np)s
			and C.CC_NOMINA in ('M020')
	union all
		select
			L.NUMERO_DE_PERSONAL,
			L.CC_NOMINA,
			(L.IMPORTE / nullif(NV.CANTIDAD::DOUBLE precision, 0))* 30 as IMPORTE,
			'NO IMPONIBLE' as TIPO,
			'NO VARIABLE' as TIPO1
		from
			BASE_LIQ L
		left join NO_VARIABL NV on
			L.NUMERO_DE_PERSONAL = NV.NUMERO_DE_PERSONAL
			and L.MARCA = NV.MARCA
		where
			L.CC_NOMINA in ('1001', '1002')
				and NV.NUMERO_DE_PERSONAL is not null
		union all
			select
				C.NP::VARCHAR,
				C.CC_NOMINA,
				C.VALOR as IMPORTE,
				'IMPONIBLE' as TIPO,
				'NO VARIABLE' as TIPO1
			from
				FLESAN_RRHH.SAP_MAESTRO_COMPENSACION C
			where
				C.NP = %(np)s
				and C.CC_NOMINA in ('1018', '1029')
		union all
			select
				*
			from
				BASE_GRATI
),
-- JB VACACIONES
VAC_BASE1 as (
select
	NP,
	MAX(cast(TO_TIMESTAMP(SUBSTRING(FECHA_VACACION, 1, 10)::BIGINT) + interval '1 DAYS' as DATE)) as FECHA
from
	FLESAN_RRHH.SAP_PONDERACION_VACACIONES
where
	NP = %(np)s
	and PONDERACION_VACACIONES > 0
group by
	NP
),
VAC_BASE as (
select
	V.NP,
	SUM(V.PONDERACION_VACACIONES) as PONDERACION,
	VB1.FECHA
from
	FLESAN_RRHH.SAP_PONDERACION_VACACIONES V
left join VAC_BASE1 VB1 on
	VB1.NP = V.NP
where
	V.NP = %(np)s
	and V.PONDERACION_VACACIONES > 0
	and cast(TO_TIMESTAMP(SUBSTRING(V.FECHA_VACACION, 1, 10)::BIGINT) + interval '1 DAYS' as DATE) = VB1.FECHA
group by
	V.NP,
	VB1.FECHA
),
JB_VACACIONES as (
select
	V.NP,
	SUM(V.PONDERACION_VACACIONES) as PONDERACION_VACACIONES,
	VB.FECHA as FECHA_VACACION,
	VB.PONDERACION
from
	FLESAN_RRHH.SAP_PONDERACION_VACACIONES V
left join VAC_BASE VB on
	VB.NP = V.NP
where
	V.NP = %(np)s
	and cast(TO_TIMESTAMP(SUBSTRING(V.FECHA_VACACION, 1, 10)::BIGINT) + interval '1 DAYS' as DATE) <= VB.FECHA
group by
	V.NP,
	VB.PONDERACION,
	VB.FECHA
)
select
	F.NUMERO_DE_PERSONAL,
	F.CC_NOMINA,
	SUM(F.IMPORTE) as IMPORTE,
	F.TIPO,
	case
		when F.CC_NOMINA = 'M020' then 'BASE'
		when F.CC_NOMINA = 'MI11' then 'GRATIFICACION'
		when F.CC_NOMINA = '1018' then 'COLACION'
		when F.CC_NOMINA = '1029' then 'MOVILIZACION'
		else 'VARIABLE'
	end as TIPO_2,
	case
		when LENGTH(MC.FECHA_ANTIGUEDAD) = 12 then cast(TO_TIMESTAMP(SUBSTRING(MC.FECHA_ANTIGUEDAD, 1, 9)::BIGINT) + interval '1 DAYS' as DATE)
		else cast(TO_TIMESTAMP(SUBSTRING(MC.FECHA_ANTIGUEDAD, 1, 10)::BIGINT) + interval '1 DAYS' as DATE)
	end as FECHA_INGRESO,
	case
		when MC.FECHA_FIN_CONTRATO = '32503680000000' then cast(TO_TIMESTAMP(SUBSTRING(MC.FECHA_FIN_CONTRATO, 1, 11)::BIGINT) + interval '1 DAYS' as DATE)
		else cast(TO_TIMESTAMP(SUBSTRING(MC.FECHA_FIN_CONTRATO, 1, 10)::BIGINT) + interval '1 DAYS' as DATE)
	end as FECHA_ESTIMADA_TERMINO,
	%(fecha_desvinculacion)s as FECHA_RETIRO,
	case
		when %(fecha_desvinculacion)s::DATE - (
case
			when LENGTH(MC.FECHA_ANTIGUEDAD) = 12 then cast(TO_TIMESTAMP(SUBSTRING(MC.FECHA_ANTIGUEDAD, 1, 9)::BIGINT) + interval '1 DAYS' as DATE)
			else cast(TO_TIMESTAMP(SUBSTRING(MC.FECHA_ANTIGUEDAD, 1, 10)::BIGINT) + interval '1 DAYS' as DATE)
		end
) >= 30 then JV.PONDERACION_VACACIONES
		else 0
	end as PONDERACION_VACACIONES,
	case
		when %(fecha_desvinculacion)s::DATE - (
case
			when LENGTH(MC.FECHA_ANTIGUEDAD) = 12 then cast(TO_TIMESTAMP(SUBSTRING(MC.FECHA_ANTIGUEDAD, 1, 9)::BIGINT) + interval '1 DAYS' as DATE)
			else cast(TO_TIMESTAMP(SUBSTRING(MC.FECHA_ANTIGUEDAD, 1, 10)::BIGINT) + interval '1 DAYS' as DATE)
		end
) >= 30 then JV.FECHA_VACACION
		else %(fecha_desvinculacion)s::DATE
	end as FECHA_VACACION,
	case
		when %(fecha_desvinculacion)s::DATE - (
case
			when LENGTH(MC.FECHA_ANTIGUEDAD) = 12 then cast(TO_TIMESTAMP(SUBSTRING(MC.FECHA_ANTIGUEDAD, 1, 9)::BIGINT) + interval '1 DAYS' as DATE)
			else cast(TO_TIMESTAMP(SUBSTRING(MC.FECHA_ANTIGUEDAD, 1, 10)::BIGINT) + interval '1 DAYS' as DATE)
		end
) >= 30 then JV.PONDERACION
		else 0
	end as PONDERACION
from
	FINAL_UNION F
left join FLESAN_RRHH.SAP_MAESTRO_COLABORADOR MC on
	MC.USER_ID::VARCHAR = %(np)s
left join JB_VACACIONES JV on
	JV.NP::VARCHAR = F.NUMERO_DE_PERSONAL
group by
	F.NUMERO_DE_PERSONAL,
	F.CC_NOMINA,
	F.TIPO,
	MC.FECHA_ANTIGUEDAD,
	MC.FECHA_TERMINO,
	MC.FECHA_FIN_CONTRATO,
	JV.PONDERACION_VACACIONES,
	JV.FECHA_VACACION,
	JV.PONDERACION
order by 
    importe asc
