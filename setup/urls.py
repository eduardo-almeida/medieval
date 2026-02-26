from django.contrib import admin
from django.urls import path
from jogo.views import dashboard, iniciar_trabalho_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('iniciar-trabalho/', iniciar_trabalho_view, name='iniciar_trabalho'),
]