from django.shortcuts import render
from django.http import JsonResponse
from .utils import get_chatgpt_response
from .models import ChatMessage
import requests
from decouple import config
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/users/login/')
def chat_interface(request):
    query = request.GET.get('query', '')
    neighborhood = request.GET.get('neighborhood', '')
    if query and neighborhood:
        ChatMessage.objects.create(user=request.user, message=f"In {neighborhood}, {query}", is_bot=False)
    messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    return render(request, 'chatbot/chatwindow.html', {'messages': messages})

@csrf_exempt
def chatbot_query(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('query', '').strip()
            neighborhood = data.get('neighborhood', '').strip()

            if user_input and neighborhood:
                ChatMessage.objects.create(user=request.user, message=user_input, is_bot=False)
                
                try:
                    headers = {
                        'Authorization': f'Bearer {config("OPENAI_API_KEY")}',
                        'OpenAI-Beta': 'assistants=v2'
                    }

                    # Send the chat completion request directly
                    completion_response = requests.post(
                        'https://api.openai.com/v1/chat/completions',
                        headers=headers,
                        json={
                            'model': 'gpt-4',
                            'messages': [
                                {'role': 'system', 'content': 'You are a helpful assistant. You are knowledgeable about all the neighborhoods of NYC and provide factual data about the different neighborhoods. do not say "as an ai, i cannot provide real time data or updates just say what you know. Limit messages to 200 words. '},
                                {'role': 'user', 'content': user_input}
                            ]
                        }
                    )
                    completion_response.raise_for_status()
                    
                    response_data = completion_response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
                    ChatMessage.objects.create(user=request.user, message=response_data, is_bot=True)
                    
                    return JsonResponse({'response': response_data})
                except requests.exceptions.RequestException as e:
                    print("Request Exception:", str(e))
                    return JsonResponse({'error': str(e)}, status=500)
            else:
                return JsonResponse({'error': 'Invalid input'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)