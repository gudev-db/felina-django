from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import uuid
from .models import ChatMessage
from .utils import AstraDBClient, get_embedding, generate_response

def get_session_id(request):
    if not request.session.get('session_id'):
        request.session['session_id'] = str(uuid.uuid4())
    return request.session['session_id']

def chat_view(request):
    session_id = get_session_id(request)
    messages = ChatMessage.objects.filter(session_id=session_id)
    return render(request, 'neia/chat.html', {'messages': messages})

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            session_id = get_session_id(request)
            
            # Salva a mensagem do usuário
            user_chat = ChatMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                role='user',
                content=user_message,
                session_id=session_id
            )
            
            # Processa a resposta
            astra_client = AstraDBClient()
            embedding = get_embedding(user_message)
            
            if embedding:
                results = astra_client.vector_search(settings.ASTRA_DB_COLLECTION, embedding)
                context = "\n".join([str(doc) for doc in results])
                
                # Gera resposta
                response = generate_response(user_message, context)
                
                # Salva a resposta do assistente
                assistant_chat = ChatMessage.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    role='assistant',
                    content=response,
                    session_id=session_id
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': response,
                    'user_message_id': user_chat.id,
                    'assistant_message_id': assistant_chat.id
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Não foi possível processar sua mensagem.'
                }, status=500)
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erro ao processar a mensagem: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

def clear_chat(request):
    if request.method == 'POST':
        session_id = get_session_id(request)
        ChatMessage.objects.filter(session_id=session_id).delete()
        return JsonResponse({'status': 'success', 'message': 'Chat limpo com sucesso'})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)
