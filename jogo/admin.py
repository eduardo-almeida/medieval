from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Personagem

@admin.register(Personagem)
class PersonagemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'nivel', 'dinheiro', 'energia', 'esta_ocupado')
    search_fields = ('nome',)