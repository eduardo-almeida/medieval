from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Personagem

@shared_task
def concluir_trabalho(personagem_id, recompensa):
    personagem = Personagem.objects.get(id=personagem_id)
    
    # Lógica de negócio
    personagem.dinheiro += recompensa
    personagem.esta_ocupado = False
    personagem.save()

    # ENVIO PARA O WEBSOCKET
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"jogador_{personagem.usuario.id}", # O canal do jogador
        {
            "type": "notificacao_trabalho", # Nome da função no Consumer
            "mensagem": f"Trabalho terminado! Ganhaste ${recompensa}",
            "dinheiro": str(personagem.dinheiro)
        }
    )