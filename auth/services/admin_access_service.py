from auth.repositories.admin_access_repository import AdminAccessRepository
from .models import GlobalAccessUser
class AdminAccessService:
    @staticmethod
    def get_admin_access(email: str):
        try:
            if not email:
                raise Exception('El parámetro email es requerido.')
            global_access_user = GlobalAccessUser.objects.filter(email=email).first()
            if global_access_user:
                return global_access_user
            access = AdminAccessRepository.get_admin_access_by_email(email)
            return access
        except Exception as e:
            raise Exception(e)
