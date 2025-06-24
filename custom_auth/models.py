from django.db import models

# Modelo para usuarios con acceso global a todos los centros de gestión
class GlobalAccessUser(models.Model):
    # Correo electrónico único del usuario con acceso global
    email = models.EmailField(unique=True)
    # Fecha de creación del registro (auditoría básica)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Indica a Django que la tabla debe crearse en el esquema 'portal_finiquitos'
        db_table = 'global_access_user'

    def __str__(self):
        # Representación legible del modelo
        return self.email

