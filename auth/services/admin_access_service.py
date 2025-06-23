from auth.repositories.admin_access_repository import AdminAccessRepository

class AdminAccessService:
    @staticmethod
    def get_admin_access(email: str):
        try:
            if not email:
                raise Exception('El parámetro email es requerido.')
            access = AdminAccessRepository.get_admin_access_by_email(email)
            return access
        except Exception as e:
            raise Exception(e)
