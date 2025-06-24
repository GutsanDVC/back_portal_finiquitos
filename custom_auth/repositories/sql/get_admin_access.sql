SELECT
 split_part(centro_coto,'-',1) as CC,
 split_part(sociedad::TEXT,'-',1) as empresa,
 case when ver_planta='x' then true else false end as ver_planta
FROM flesan_rrhh.tabla_encargados_cc AS tec
where tec.correo= %(correo)s
and tec.administrador='x' 
