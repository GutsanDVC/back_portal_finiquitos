# Generated by Django 4.2.11 on 2025-06-24 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SapMaestroColaborador",
            fields=[
                ("user_id", models.FloatField(primary_key=True, serialize=False)),
                (
                    "empl_status",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("first_name", models.CharField(blank=True, max_length=255, null=True)),
                ("last_name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "second_last_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "middle_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "national_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "correo_flesan",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "correo_gmail",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("run", models.CharField(blank=True, max_length=255, null=True)),
                ("empresa", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "centro_costo",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_cod_cargo",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "fecha_ingreso",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("ubicacion", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "nombre_centro_costo",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "departamento",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "nombre_departamento",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("division", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "nombre_division",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "external_cod_tipo_contrato",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "fecha_fin_contrato",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "fecha_termino",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("forma_pago", models.IntegerField(blank=True, null=True)),
                ("np_lider", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "fecha_antiguedad",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "fecha_registro_termino",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "id_clasificacion_gasto",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("tipo_gasto", models.CharField(blank=True, max_length=255, null=True)),
                ("horario", models.CharField(blank=True, max_length=255, null=True)),
                ("genero", models.CharField(blank=True, max_length=255, null=True)),
                ("pais", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "id_pais_nacimiento",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "eventreason",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "fecha_nacimiento",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "fecha_ingreso_original",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("fecha_nacimiento_date", models.DateField(blank=True, null=True)),
                (
                    "fecha_ingreso_original_date",
                    models.DateField(blank=True, null=True),
                ),
                ("fecha_ingreso_date", models.DateField(blank=True, null=True)),
                ("fecha_fin_contrato_date", models.DateField(blank=True, null=True)),
                ("fecha_termino_date", models.DateField(blank=True, null=True)),
                ("fecha_antiguedad_date", models.DateField(blank=True, null=True)),
                (
                    "fecha_registro_termino_date",
                    models.DateField(blank=True, null=True),
                ),
            ],
            options={
                "verbose_name": "Colaborador SAP (DW)",
                "verbose_name_plural": "Colaboradores SAP (DW)",
                "db_table": "flesan_rrhh.sap_maestro_colaborador",
                "managed": False,
            },
        ),
    ]
