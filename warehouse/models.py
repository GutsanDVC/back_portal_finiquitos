from django.db import models

class SapMaestroColaborador(models.Model):
    """
    Modelo de solo lectura que representa la tabla flesan_rrhh.sap_maestro_colaborador
    en el Data Warehouse. Permite consultar datos maestros de colaboradores para
    reportes y procesos, pero no permite crear, modificar ni borrar registros desde Django.
    """
    user_id = models.FloatField(primary_key=True)  # ID único del usuario (double precision)
    empl_status = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    second_last_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    national_id = models.CharField(max_length=255, blank=True, null=True)
    correo_flesan = models.CharField(max_length=255, blank=True, null=True)
    correo_gmail = models.CharField(max_length=255, blank=True, null=True)
    run = models.CharField(max_length=255, blank=True, null=True)
    empresa = models.CharField(max_length=255, blank=True, null=True)
    centro_costo = models.CharField(max_length=255, blank=True, null=True)
    external_cod_cargo = models.CharField(max_length=255, blank=True, null=True)
    fecha_ingreso = models.CharField(max_length=255, blank=True, null=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    nombre_centro_costo = models.CharField(max_length=255, blank=True, null=True)
    departamento = models.CharField(max_length=255, blank=True, null=True)
    nombre_departamento = models.CharField(max_length=255, blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    nombre_division = models.CharField(max_length=255, blank=True, null=True)
    external_cod_tipo_contrato = models.CharField(max_length=255, blank=True, null=True)
    fecha_fin_contrato = models.CharField(max_length=255, blank=True, null=True)
    fecha_termino = models.CharField(max_length=255, blank=True, null=True)
    forma_pago = models.IntegerField(blank=True, null=True)
    np_lider = models.CharField(max_length=255, blank=True, null=True)
    fecha_antiguedad = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro_termino = models.CharField(max_length=255, blank=True, null=True)
    id_clasificacion_gasto = models.CharField(max_length=255, blank=True, null=True)
    tipo_gasto = models.CharField(max_length=255, blank=True, null=True)
    horario = models.CharField(max_length=255, blank=True, null=True)
    genero = models.CharField(max_length=255, blank=True, null=True)
    pais = models.CharField(max_length=255, blank=True, null=True)
    id_pais_nacimiento = models.CharField(max_length=255, blank=True, null=True)
    eventreason = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.CharField(max_length=255, blank=True, null=True)
    fecha_ingreso_original = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento_date = models.DateField(blank=True, null=True)
    fecha_ingreso_original_date = models.DateField(blank=True, null=True)
    fecha_ingreso_date = models.DateField(blank=True, null=True)
    fecha_fin_contrato_date = models.DateField(blank=True, null=True)
    fecha_termino_date = models.DateField(blank=True, null=True)
    fecha_antiguedad_date = models.DateField(blank=True, null=True)
    fecha_registro_termino_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False  # Django no crea ni modifica esta tabla
        db_table = 'flesan_rrhh.sap_maestro_colaborador'  # Esquema y tabla exactos en el DW
        verbose_name = 'Colaborador SAP (DW)'
        verbose_name_plural = 'Colaboradores SAP (DW)'

    def __str__(self):
        # Representación legible para administración y debug
        return f"{self.user_id} - {self.first_name} {self.last_name}"
