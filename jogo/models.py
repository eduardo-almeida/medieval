from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Personagem(models.Model):
    # 1. Relacionamento com a conta do utilizador
    # Usamos OneToOne para que cada conta tenha apenas um cowboy
    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="personagem"
    )
    
    # 2. Informações Básicas
    nome = models.CharField(max_length=50, unique=True)
    nivel = models.PositiveIntegerField(default=1)
    experiencia = models.BigIntegerField(default=0)
    
    # 3. Recursos (Economia e Gameplay)
    # DecimalField é o padrão ouro para dinheiro em jogos comerciais
    dinheiro = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Energia limitada para realizar trabalhos
    energia = models.IntegerField(
        default=100, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # 4. Estado de Jogo (Lógica de Tempo Real)
    # Estes campos controlam se o jogador está na mina, floresta, etc.
    esta_ocupado = models.BooleanField(default=False)
    tarefa_atual = models.CharField(max_length=100, null=True, blank=True)
    data_conclusao_tarefa = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Personagens"

    def __str__(self):
        return f"{self.nome} (Nível {self.nivel})"

    # Método útil para o seu Frontend saber quanto tempo falta
    def tempo_restante(self):
        if self.data_conclusao_tarefa and self.data_conclusao_tarefa > timezone.now():
            diff = self.data_conclusao_tarefa - timezone.now()
            return int(diff.total_seconds())
        return 0