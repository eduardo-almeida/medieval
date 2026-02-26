from django.contrib import admin
from .models import Personagem, Local

@admin.register(Personagem)
class PersonagemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'nivel', 'dinheiro', 'energia', 'esta_ocupado')
    search_fields = ('nome',)

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'posicao_x', 'posicao_y')