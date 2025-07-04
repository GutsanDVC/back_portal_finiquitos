from django.urls import path
from .views.admin_access_view import AdminAccessView
from .views.google_token_validate_view import GoogleTokenValidateView
from .views.global_access_user_create_view import GlobalAccessUserCreateView
from .views.global_access_user_crud_view import GlobalAccessUserListCreateView, GlobalAccessUserDetailView

urlpatterns = [
    path('', GoogleTokenValidateView.as_view(), name='google-validate-token'),
    path('admin-access/', AdminAccessView.as_view(), name='admin-access'),
    # Endpoint antiguo para agregar usuarios globales (puedes eliminarlo si ya no se usa)
    path('global-access-users/add/', GlobalAccessUserCreateView.as_view(), name='global-access-user-add'),
    # Endpoints CRUD completos
    path('global-access-users/', GlobalAccessUserListCreateView.as_view(), name='global-access-user-list-create'),
    path('global-access-users/<str:np>/', GlobalAccessUserDetailView.as_view(), name='global-access-user-detail'),
]
