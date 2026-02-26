from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
from .models import Personagem, Item, Inventario

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

@shared_task
def concluir_viagem(personagem_id, novo_x, novo_y):
    from .models import Personagem
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    
    personagem = Personagem.objects.get(id=personagem_id)
    personagem.posicao_x = novo_x
    personagem.posicao_y = novo_y
    personagem.esta_ocupado = False
    personagem.tarefa_atual = None
    personagem.save()

    # Avisar o frontend via WebSocket que o Cowboy chegou!
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"jogador_{personagem.usuario.id}",
        {
            "type": "notificacao_trabalho", # Reutilizamos o mesmo tipo de mensagem
            "mensagem": f"Chegaste ao teu destino em ({novo_x}, {novo_y})!",
            "dinheiro": str(personagem.dinheiro) # Atualiza a carteira por segurança
        }
    )

@shared_task
def concluir_trabalho(personagem_id, recompensa_dinheiro):
    from .models import Personagem
    personagem = Personagem.objects.get(id=personagem_id)
    
    # 1. Adicionar Dinheiro
    personagem.dinheiro += recompensa_dinheiro
    
    # 2. Lógica de Item (30% de chance de achar algo)
    item_ganho_nome = ""
    if random.random() <= 0.30:
        # Tenta pegar um item aleatório do banco de dados
        item_sorteado = Item.objects.order_by('?').first()
        if item_sorteado:
            inv, created = Inventario.objects.get_or_create(
                personagem=personagem, 
                item=item_sorteado
            )
            if not created:
                inv.quantidade += 1
                inv.save()
            item_ganho_nome = item_sorteado.nome

    personagem.esta_ocupado = False
    personagem.save()