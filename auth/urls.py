from django.urls import path
from .views.admin_access_view import AdminAccessView
from .views.google_token_validate_view import GoogleTokenValidateView

urlpatterns = [
    path('', GoogleTokenValidateView.as_view(), name='google-validate-token'),
    path('admin-access/', AdminAccessView.as_view(), name='admin-access'),
]
