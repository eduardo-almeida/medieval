from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import Personagem, Local, Inventario
from .tasks import concluir_viagem

@login_required
def dashboard(request):
    from .models import Personagem
    try:
        personagem = Personagem.objects.get(usuario=request.user)
        return render(request, 'jogo/dashboard.html', {'personagem': personagem})
    except Personagem.DoesNotExist:
        # Se o admin não criou o personagem ainda, redirecionamos ou damos erro
        return render(request, 'jogo/dashboard.html', {'error': 'Crie um personagem no Admin!'})

@login_required # Garante que só quem está logado pode trabalhar
def iniciar_trabalho_view(request):
    print(f"Método recebido: {request.method}") # Debug
    
    if request.method == "POST":
        from .models import Personagem
        from .tasks import concluir_trabalho
        
        try:
            personagem = Personagem.objects.get(usuario=request.user)
            
            if personagem.esta_ocupado:
                print("Erro: Personagem já está ocupado!")
                return JsonResponse({"status": "error", "motivo": "ocupado"}, status=400)

            # Inicia o processo
            personagem.esta_ocupado = True
            personagem.save()
            
            concluir_trabalho.apply_async(args=[personagem.id, 50], countdown=5)
            print(f"Sucesso! Tarefa enviada para o personagem {personagem.nome}")
            return JsonResponse({"status": "ok"})

        except Personagem.DoesNotExist:
            print("Erro: O utilizador logado não tem um Personagem criado!")
            return JsonResponse({"status": "error", "motivo": "sem_personagem"}, status=404)
            
    print("Erro: O pedido não foi via POST!")
    return JsonResponse({"status": "error", "motivo": "metodo_invalido"}, status=400)

def mapa(request):
    personagem = Personagem.objects.get(usuario=request.user)
    locais = Local.objects.all()
    return render(request, 'jogo/mapa.html', {'personagem': personagem, 'locais': locais})

def iniciar_viagem_view(request):
    if request.method == "POST":
        dados = json.loads(request.body)
        local_destino = Local.objects.get(id=dados['local_id'])
        personagem = Personagem.objects.get(usuario=request.user)
        
        if not personagem.esta_ocupado:
            # Calcula o tempo usando a nossa função matemática
            tempo_segundos = personagem.calcular_tempo_viagem(
                local_destino.posicao_x, 
                local_destino.posicao_y
            )
            
            personagem.esta_ocupado = True
            personagem.tarefa_atual = f"Viajando para {local_destino.nome}"
            personagem.save()
            
            # Agenda a chegada
            concluir_viagem.apply_async(
                args=[personagem.id, local_destino.posicao_x, local_destino.posicao_y],
                countdown=tempo_segundos
            )
            
            return JsonResponse({"status": "ok", "tempo": tempo_segundos})
            
    return JsonResponse({"status": "error"}, status=400)

def inventario_view(request):
    personagem = Personagem.objects.get(usuario=request.user)
    # Pegamos todos os itens da mochila desse personagem
    itens_mochila = Inventario.objects.filter(personagem=personagem)
    return render(request, 'jogo/inventario.html', {
        'personagem': personagem, 
        'itens': itens_mochila
    })