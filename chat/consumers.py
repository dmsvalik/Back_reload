import json

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import MessageModel, ChatModel
from .serializers import MessageSerializer

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        """
        Fetch last messages from this chat (load history)
        """
        messages = self.current_chat.messages.all()
        content = {
            'command': 'fetch_messages',
            'messages': MessageSerializer(messages, many=True).data
        }
        self.display_content(content)

    def new_message(self, data):
        """
        Send new message to this chat
        """
        sender_email = data['from']
        sender = User.objects.get(email=sender_email)
        message = MessageModel.objects.create(
            from_user=sender,
            text_content=data['message'],
            to_chat=self.current_chat
        )
        content = {
            'command': 'new_message',
            'message': MessageSerializer(message).data
        }
        return self.send_message_to_group(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        """
        Connect to chat
        """
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_group_name = f"chat_{self.chat_id}"
        self.current_chat = get_object_or_404(ChatModel, pk=self.chat_id)

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """
        Leave chat
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name, self.channel_name
        )

    def receive(self, text_data):
        """
        Receive message from WebSocket client
        """
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message_to_group(self, message):
        """
        Send message to chat group
        """
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                "type": "receive.message",
                "message": message
            }
        )

    def display_content(self, content):
        """
        Send content to WebSocket to display it
        """
        self.send(
            text_data=json.dumps(content)
        )

    def receive_message(self, event):
        """
        Receive message from chat group
        """
        message = event["message"]
        self.send(
            text_data=json.dumps(message)
        )
