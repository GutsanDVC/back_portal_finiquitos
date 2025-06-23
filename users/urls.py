from django.urls import path
from .views import ApplicationUserCreateView

urlpatterns = [
    path('create/', ApplicationUserCreateView.as_view(), name='user-create'),
]