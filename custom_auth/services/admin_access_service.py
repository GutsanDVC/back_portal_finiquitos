from custom_auth.repositories.admin_access_repository import AdminAccessRepository
class AdminAccessService:
    @staticmethod
    def get_admin_access(email: str):
        try:
            if not email:
                raise Exception('El parámetro email es requerido.')
            from custom_auth.repositories.global_access_user_repository import obtener_usuario_por_email
            email=email.lower()
            global_access_user = obtener_usuario_por_email(email)
            print(global_access_user)
            if global_access_user:
                return [{"global_access": True}]
            access = AdminAccessRepository.get_admin_access_by_email(email)
            return access
        except Exception as e:
            raise Exception(e)
