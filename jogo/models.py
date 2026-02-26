import math
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Local(models.Model):
    nome = models.CharField(max_length=100)
    posicao_x = models.IntegerField(default=0)
    posicao_y = models.IntegerField(default=0)
    descricao = models.TextField(blank=True)
    imagem_mapa = models.CharField(max_length=100, default="icon-default.png")

    class Meta:
        verbose_name_plural = "Locais"

    def __str__(self):
        return f"{self.nome} ({self.posicao_x}, {self.posicao_y})"

class Personagem(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personagem")
    nome = models.CharField(max_length=50, unique=True)
    nivel = models.PositiveIntegerField(default=1)
    experiencia = models.BigIntegerField(default=0)
    dinheiro = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    energia = models.IntegerField(
        default=100, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # --- SISTEMA DE MOVIMENTAÇÃO ---
    posicao_x = models.IntegerField(default=0)
    posicao_y = models.IntegerField(default=0)
    
    # Estado de Jogo
    esta_ocupado = models.BooleanField(default=False)
    tarefa_atual = models.CharField(max_length=100, null=True, blank=True)
    data_conclusao_tarefa = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Personagens"

    def __str__(self):
        return f"{self.nome} (Nível {self.nivel})"

    # --- FUNÇÃO MATEMÁTICA DE VIAGEM ---
    def calcular_tempo_viagem(self, destino_x, destino_y):
        """
        Calcula a distância euclidiana entre a posição atual e o destino.
        Fórmula: sqrt((x2-x1)^2 + (y2-y1)^2)
        """
        distancia = math.sqrt(
            (destino_x - self.posicao_x)**2 + 
            (destino_y - self.posicao_y)**2
        )
        # Supondo que o cowboy anda 1 unidade de mapa por segundo
        segundos_necessarios = int(distancia)
        return segundos_necessarios

    def tempo_restante(self):
        if self.data_conclusao_tarefa and self.data_conclusao_tarefa > timezone.now():
            diff = self.data_conclusao_tarefa - timezone.now()
            return int(diff.total_seconds())
        return 0

class Item(models.Model):
    TIPOS = (
        ('FERRAMENTA', 'Ferramenta'),
        ('RECURSO', 'Recurso'),
        ('EQUIPAMENTO', 'Equipamento'),
    )
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='RECURSO')
    imagem_icon = models.CharField(max_length=100, default="item-default.png")

    def __str__(self):
        return self.nome

class Inventario(models.Model):
    personagem = models.ForeignKey(Personagem, on_delete=models.CASCADE, related_name="mochila")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.item.nome} de {self.personagem.nome}"