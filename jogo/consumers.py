import json
from channels.generic.websocket import AsyncWebsocketConsumer

class JogoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Cada jogador terá o seu próprio "canal" baseado no ID de utilizador
        self.user_id = self.scope["user"].id
        self.group_name = f"jogador_{self.user_id}"

        # Entra no grupo (canal) do jogador
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Sai do grupo ao fechar o jogo
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Este método é chamado quando o Celery envia uma mensagem para este grupo
    async def notificacao_trabalho(self, event):
        await self.send(text_data=json.dumps({
            'tipo': 'TRABALHO_CONCLUIDO',
            'mensagem': event['mensagem'],
            'dinheiro': event['dinheiro']
        }))