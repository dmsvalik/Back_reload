from datetime import datetime
import json

from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatMessage, Conversation
from .serializers import MessageSerializer


User = get_user_model()


def get_serialized_data(messages):
    serializer = MessageSerializer(messages, many=True)
    return serializer.data


class AsyncChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.chat_id = None
        self.chat_group_name = None
        self.conversation = None
        self.messages_for_db = []
        self.user = None

    async def connect(self):
        """
        Открытие соединения.
        Забираем из скоупа нужные данные, делаем проверки.
        По итогу прохождения проверок соглашаемся либо закрываем
        хендшейк.
        """

        if self.scope["user"] and self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            if self.user is None:
                await self.close()
                return
        else:
            await self.close()
            return

        self.chat_id = self.scope["url_route"]["kwargs"].get("chat_id")

        if await Conversation.objects.filter(pk=self.chat_id).aexists():
            self.conversation = await Conversation.objects.aget(
                pk=self.chat_id
            )
            if self.conversation.is_blocked:
                await self.close()
                return
        else:
            await self.close()
            return

        if (
            self.user.role == "contractor"
            and self.conversation.is_match is False
        ):
            await self.close()
            return

        self.chat_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        """
        Вызывается при разрыве вебсокетного соединения.
        Сбрасывает накопленные сообщения в базу одним запросом.
        """

        await ChatMessage.objects.abulk_create(self.messages_for_db)

        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name,
        )

    async def chat_message(self, event):
        """
        Отправка одного конкретного сообщения.
        """

        message = event.get("message")
        sender = event.get("sender")
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": sender,
                },
                ensure_ascii=False,
            ),
        )

    async def display_content(self, content):
        """
        Send content to WebSocket to display it
        """
        await self.send(text_data=json.dumps(content))

    async def fetch_messages(self, data):
        """
        Fetch last messages from this chat (load history)
        """
        messages = self.conversation.messages.all()
        content = {
            "messages": await sync_to_async(get_serialized_data)(messages)
        }
        await self.display_content(content)

    async def new_message(self, data):
        """
        Send new message to this chat
        """
        sender = self.user
        message = data.get("message")
        self.messages_for_db.append(
            ChatMessage(
                conversation=self.conversation,
                sender=sender,
                text=message,
                sent_at=datetime.now(),
            )
        )
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": "chat.message",
                "message": message,
                "sender": sender.email,
            },
        )

    commands = {"fetch_messages": fetch_messages, "new_message": new_message}

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        if message:
            await self.commands[text_data_json["command"]](
                self, text_data_json
            )
