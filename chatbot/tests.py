import openai
import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ChatMessage

User = get_user_model()

class ChatbotTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_chat_interface_view(self):
        response = self.client.get(reverse('chat_interface'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatbot/chatwindow.html')

    def test_chatbot_query_view(self):
        response = self.client.post(reverse('chatbot_query'), {
            'query': 'Hello',
            'neighborhood': 'Manhattan'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())

    def test_chat_message_creation(self):
        ChatMessage.objects.create(user=self.user, message='Test message', is_bot=False)
        self.assertEqual(ChatMessage.objects.count(), 1)
        self.assertEqual(ChatMessage.objects.first().message, 'Test message')

# Load the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


def test_openai_api():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, OpenAI!"}],
        )
        print("API Response:", response.choices[0].message["content"].strip())
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    test_openai_api()
