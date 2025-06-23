from django.db import models

# Modelo para la tabla de aplicaciones empresariales
class Application(models.Model):
    id_aplicacion = models.IntegerField(primary_key=True, db_column='id_aplicacion')  # Clave primaria
    name = models.CharField(max_length=50, db_column='nombre')  # Nombre de la aplicación
    description = models.CharField(max_length=200, blank=True, null=True, db_column='descripcion')  # Descripción de la aplicación
    start_date = models.DateField(db_column='fecha_ini')  # Fecha de inicio
    end_date = models.DateField(blank=True, null=True, db_column='fecha_fin')  # Fecha de término (opcional)

    class Meta:
        db_table = 'aplicacion'
        managed = False  
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return self.name

# Modelo para la tabla de usuarios asociados a aplicaciones
class ApplicationUser(models.Model):
    id_aplicacion_usuario = models.BigAutoField(primary_key=True, db_column='id_aplicacion_usuario', serialize=False)
    application = models.ForeignKey(Application, db_column='id_aplicacion', on_delete=models.DO_NOTHING)
    username = models.CharField(max_length=50, db_column='username')
    fecha_ini = models.DateField(db_column='fecha_ini')
    fecha_fin = models.DateField(blank=True, null=True, db_column='fecha_fin')
    name = models.CharField(max_length=255, db_column='name')
    provider = models.CharField(max_length=255, db_column='provider', blank=True, null=True)
    provider_id = models.CharField(max_length=255, db_column='provider_id', blank=True, null=True)
    remember_token = models.CharField(max_length=255, db_column='remember_token', blank=True, null=True)
    estado_sesion = models.IntegerField(db_column='estado_sesion')
    fecha_validacion = models.DateField(blank=True, null=True, db_column='fecha_validacion')
    dni = models.CharField(max_length=50, db_column='dni', blank=True, null=True)
    nombres = models.CharField(max_length=255, db_column='nombres', blank=True, null=True)
    apellidos = models.CharField(max_length=255, db_column='apellidos', blank=True, null=True)
    estado_validacion = models.IntegerField(db_column='estado_validacion')
    pais = models.CharField(max_length=100, db_column='pais', blank=True, null=True)
    refresh_token = models.CharField(max_length=255, db_column='refresh_token', blank=True, null=True)
    avatar = models.CharField(max_length=255, db_column='avatar', blank=True, null=True)
    password = models.CharField(max_length=1024, db_column='password', blank=True, null=True)
    old_id = models.IntegerField(blank=True, null=True, db_column='old_id')
    fecha_purga = models.DateField(blank=True, null=True, db_column='fecha_purga')

    class Meta:
        db_table = 'aplicacion_usuario'
        managed = False
        verbose_name = "Application User"
        verbose_name_plural = "Application Users"

    def __str__(self):
        return self.username

# Modelo para roles dentro de una aplicación
class Role(models.Model):
    application = models.ForeignKey(Application, db_column='id_aplicacion', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    attribute_list = models.TextField(blank=True, null=True) 

    class Meta:
        db_table = 'rol_aplicacion'
        managed = False
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name

# Modelo para la relación entre usuario y rol (muchos a muchos)
class UserRole(models.Model):
    application_user = models.ForeignKey(ApplicationUser, db_column='id_aplicacion_usuario', on_delete=models.DO_NOTHING)
    role = models.ForeignKey(Role, db_column='id_rol', on_delete=models.DO_NOTHING)
    company_id = models.IntegerField()
    permitted_object = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    business_unit_id = models.CharField(max_length=10)
    user_id = models.IntegerField()
    country = models.CharField(max_length=10)
    status = models.IntegerField()

    class Meta:
        db_table = 'usuario_rol'
        managed = False
        verbose_name = "User Role"
        verbose_name_plural = "User Roles"

    def __str__(self):
        return f"{self.application_user} - {self.role}"

# Nota: Todos los modelos usan managed=False para reflejar que las tablas ya existen y no deben ser gestionadas por Django.
# Las relaciones ForeignKey usan on_delete=models.DO_NOTHING para evitar borrados en cascada accidentales.
