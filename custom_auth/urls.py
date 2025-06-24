from django.urls import path
from .views.admin_access_view import AdminAccessView
from .views.google_token_validate_view import GoogleTokenValidateView
from .views.global_access_user_create_view import GlobalAccessUserCreateView

urlpatterns = [
    path('', GoogleTokenValidateView.as_view(), name='google-validate-token'),
    path('admin-access/', AdminAccessView.as_view(), name='admin-access'),
    # Endpoint para agregar nuevos usuarios con acceso global
    path('global-access-users/add/', GlobalAccessUserCreateView.as_view(), name='global-access-user-add'),
]
