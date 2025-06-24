SELECT 
    user_id, 
    empl_status, 
    first_name, 
    last_name,
    national_id,
    correo_flesan, 
    correo_gmail,  
    empresa, 
    centro_costo, 
    external_cod_cargo, 
    fecha_ingreso_date,
    nombre_centro_costo,
    external_cod_tipo_contrato, 
    fecha_fin_contrato, 
    fecha_termino,
    nombre_cargo,
    planta_noplanta
FROM 
    flesan_rrhh.sap_maestro_colaborador colaboradores
left join 
flesan_rrhh.sap_maestro_cargos cargos
on
colaboradores.external_cod_cargo =cargos.external_code
    WHERE 
    empl_status='41111'
    --filter--
    order by  user_id

