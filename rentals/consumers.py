# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from users.models import User
from .models import Message


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        if self.scope["user"].is_authenticated:
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        recipient_id = text_data_json.get('recipient_id') 

        # Create a Message instance
        sender = self.scope["user"]

        recipient = User.objects.get(id=recipient_id)
        Message.objects.create(sender=sender, recipient=recipient, content=message)

        # Broadcast message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': self.scope["user"].username,
            'recipient': recipient.username,
        }))
