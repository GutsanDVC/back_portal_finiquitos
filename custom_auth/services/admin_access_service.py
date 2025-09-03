from custom_auth.repositories.admin_access_repository import AdminAccessRepository
from utils.txt_logger import writeTxtLog
from custom_auth.repositories.global_access_user_repository import obtener_usuario_por_email
class AdminAccessService:
    @staticmethod
    def get_admin_access(email: str):
        try:
            if not email:
                raise Exception('El parámetro email es requerido.')
            
            email=email.lower()
            global_access_user = obtener_usuario_por_email(email)
            writeTxtLog("global_access_user",global_access_user,"INFO")
            if global_access_user:
                return [{"global_access": True}]
            access = AdminAccessRepository.get_admin_access_by_email(email)
            writeTxtLog("access",access,"INFO")
            return access
        except Exception as e:
            raise Exception(e)
