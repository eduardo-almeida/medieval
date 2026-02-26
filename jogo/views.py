from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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