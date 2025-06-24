"""
Configuraci n de URLs para el proyecto portal_finiquitos.

La lista `urlpatterns` enruta URLs a vistas. Para obtener m s informaci n, por favor consulta:
    https://docs.djangoproject.com/es/5.2/topics/http/urls/
Ejemplos:
Vistas de funciones
    1. Agrega una importaci n:  from my_app import views
    2. Agrega una URL a urlpatterns:  path('', views.home, name='home')
Vistas basadas en clases
    1. Agrega una importaci n:  from other_app.views import Home
    2. Agrega una URL a urlpatterns:  path('', Home.as_view(), name='home')
Incluir otra configuraci n de URL
    1. Importa la funci n include(): from django.urls import include, path
    2. Agrega una URL a urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users import urls as users_urls
from warehouse import urls as warehouse_urls
from settlements import urls as settlements_urls
from custom_auth import urls as auth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # Endpoint API para warehouse (DW)
    path('api/warehouse/', include(warehouse_urls)),
    path('api/settlements/', include(settlements_urls)),
    path('api/users/', include(users_urls)),
    path('api/auth/', include(auth_urls)),
]
