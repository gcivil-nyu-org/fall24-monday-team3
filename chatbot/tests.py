# import openai
# import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ChatMessage
from unittest.mock import patch
import json
import requests

User = get_user_model()


class ChatbotTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_chat_interface_view(self):
        """Test the chat interface view"""
        response = self.client.get(reverse("chat_interface"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chatbot/chatwindow.html")

    def test_chat_interface_with_query(self):
        """Test chat interface with query parameters"""
        response = self.client.get(
            reverse("chat_interface"),
            {'query': 'test query', 'neighborhood': 'Manhattan'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ChatMessage.objects.filter(user=self.user).exists())

    def test_chat_message_str_representation(self):
        """Test string representation of ChatMessage"""
        # Test bot message
        bot_message = ChatMessage.objects.create(
            user=self.user,
            message="Bot message",
            is_bot=True
        )
        self.assertEqual(str(bot_message), "Bot: Bot message")

        # Test user message
        user_message = ChatMessage.objects.create(
            user=self.user,
            message="User message",
            is_bot=False
        )
        self.assertEqual(str(user_message), f"{self.user.username}: User message")

    @patch('requests.post')
    def test_chatbot_query_success(self, mock_post):
        """Test successful chatbot query"""
        class MockResponse:
            def __init__(self):
                self.status_code = 200

            def json(self):
                return {
                    "choices": [
                        {
                            "message": {
                                "content": "Test response"
                            }
                        }
                    ]
                }

            def raise_for_status(self):
                pass

        mock_post.return_value = MockResponse()

        response = self.client.post(
            reverse("chatbot_query"),
            data=json.dumps({
                "query": "test query",
                "neighborhood": "Manhattan"
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "Test response"})

    def test_chatbot_query_invalid_json(self):
        """Test invalid JSON input"""
        response = self.client.post(
            reverse("chatbot_query"),
            data="invalid json",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid JSON"})

    def test_chatbot_query_empty_input(self):
        """Test empty input"""
        response = self.client.post(
            reverse("chatbot_query"),
            data=json.dumps({"query": "", "neighborhood": ""}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid input"})

    def test_chatbot_query_invalid_method(self):
        """Test invalid HTTP method"""
        response = self.client.get(reverse("chatbot_query"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid request"})

    @patch('requests.post')
    def test_chatbot_query_api_error(self, mock_post):
        """Test API error handling"""
        mock_post.side_effect = requests.exceptions.RequestException("API Error")

        response = self.client.post(
            reverse("chatbot_query"),
            data=json.dumps({
                "query": "test query",
                "neighborhood": "Manhattan"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "API Error"})

    @patch('requests.post')
    def test_chatbot_query_general_error(self, mock_post):
        """Test general error handling"""
        mock_post.side_effect = Exception("General Error")

        response = self.client.post(
            reverse("chatbot_query"),
            data=json.dumps({
                "query": "test query",
                "neighborhood": "Manhattan"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "General Error"})

    def test_unauthenticated_access(self):
        """Test access without authentication"""
        self.client.logout()
        response = self.client.get(reverse("chat_interface"))
        self.assertRedirects(response, '/users/login/?next=/chatbot/')
