from django.contrib import admin
from .models import Personagem, Local, Item, Inventario  # Adicione Item e Inventario aqui

@admin.register(Personagem)
class PersonagemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'nivel', 'dinheiro', 'esta_ocupado', 'posicao_x', 'posicao_y')
    search_fields = ('nome',)

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'posicao_x', 'posicao_y')

# Registro do Novo Sistema de Itens
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'valor_venda')
    list_filter = ('tipo',)
    search_fields = ('nome',)

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('personagem', 'item', 'quantidade')
    list_filter = ('personagem', 'item')