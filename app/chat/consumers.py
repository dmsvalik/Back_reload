from datetime import datetime
import json

from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Conversation
from .redis_client import RedisClient
from .serializers import MessageSerializer
from .utils import (
    generate_message_hash,
    load_message_history_to_redis,
    store_messages_to_db,
)


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
        # все сообщения, которые мы хотим скинуть в базу по завершению
        self.hashes_for_db = []
        self.user = None
        self.redis = RedisClient.from_settings()

    async def connect(self):
        """
        Выполняется на открытии соединения.
        Сюда убраны проверки на аутентификацию, наличия чата
        и его блокировки, а так же инициирует наполнение редиса данными.
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
            # подгружаем все сообщения из бд в редиску
            await sync_to_async(load_message_history_to_redis)(
                self.redis,
                self.chat_id,
                None,
                None,
            )
        else:
            await self.close()
            return

        if (
            self.user.role == "contractor"
            and not self.conversation.messages.filter(
                sender__role="client"
            ).aexists()
        ):
            await self.close()
            return

        self.chat_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name,
        )

        await self.accept(self.scope["custom_subprotocol"])

    async def disconnect(self, code):
        """
        Выполняется при разрыве соединения
        Так же отправляет хеши сообщений на сброс в базу данных
        из редиса
        """
        try:
            await sync_to_async(store_messages_to_db)(
                self.chat_group_name, self.hashes_for_db
            )

            await self.channel_layer.group_discard(
                self.chat_group_name,
                self.channel_name,
            )

        except Exception as e:
            # FIXME! залоггировать
            print(e)

    async def chat_message(self, event):
        """
        Метод, с помощью которого выполняется отправка
        всем подписчикам layer-а
        """
        await self.send(
            text_data=json.dumps(
                {
                    "text": event.get("text"),
                    "sender": event.get("sender"),
                    "sent_at": event.get("sent_at"),
                    "hashcode": event.get("hashcode"),
                    "is_read": event.get("is_read"),
                },
                ensure_ascii=False,
            ),
        )

    async def fetch_messages(self):
        """Старый метод получения истории сообщений из базы"""
        messages = self.conversation.messages.all()
        content = {
            "messages": await sync_to_async(get_serialized_data)(messages)
        }
        await self.send(text_data=json.dumps(content))

    async def fetch_messages_redis(self):
        """
        Метод получения истории сообщений из редиса
        """
        messages = []
        redis_keys = self.redis.search_by_pattern("chat_" + self.chat_id + "*")
        for key in redis_keys:
            stored = self.redis.get_message_by_key(key)
            stored["hashcode"] = key.split(":")[1]
            messages.append(stored)
        await self.send(text_data=json.dumps(messages))

    async def new_message(self, message):
        """
        Метод отправки нового сообщения
        Генерит для него хеш, сохраняет в редис и отправляет
        подписчикам layer-а
        """
        sender = self.user

        message_to_send = {
            "text": message,
            "sender": sender.email,
            "sent_at": str(datetime.now()),
            "is_read": str(False),
        }

        new_hash = generate_message_hash(message_to_send)
        while new_hash in self.hashes_for_db:
            new_hash = generate_message_hash(message_to_send)

        self.hashes_for_db.append(new_hash)

        message_to_send["hashcode"] = new_hash

        self.redis.store_message(
            self.chat_group_name, new_hash, message_to_send
        )

        message_to_send["type"] = "chat.message"

        await self.channel_layer.group_send(
            self.chat_group_name,
            message_to_send,
        )

    @staticmethod
    def validate_hashcodes(hashcodes):
        """Валидация хешей чтобы не курочить редис и бд"""
        if not isinstance(hashcodes, list):
            return None
        result = []
        for element in hashcodes:
            if not isinstance(element, str):
                continue
            result.append(element)
        return result

    async def read_messages(self, hashcodes) -> (bool, str):
        """Метод разметки сообщений прочитанными"""
        try:
            hashcodes = self.validate_hashcodes(hashcodes)
            messages_to_mark_read = dict()
            for code in hashcodes:
                message = self.redis.get_message(self.chat_group_name, code)
                if (
                    message.get("sender")
                    and message.get("sender") != self.user.email
                ):
                    message["is_read"] = str(True)
                    messages_to_mark_read[code] = message
            self.redis.store_multiple_messages(
                self.chat_group_name, messages_to_mark_read
            )
            return True, "OK"
        except Exception as e:
            # FIXME! залоггировать
            return False, e

    async def receive(self, text_data=None, bytes_data=None):
        """
        Метод вызывается при получении сообщения извне
        """
        text_data_json = json.loads(text_data)
        command = text_data_json.get("command")
        if not command:
            await self.send(
                text_data=json.dumps(
                    {
                        "status": "fail",
                        "error": "command was not provided",
                    }
                )
            )

        match command:
            # команда чтения сообщений
            case "read_messages":
                hashcodes = text_data_json.get("hashcodes")
                if not hashcodes:
                    await self.send(
                        text_data=json.dumps(
                            {
                                "status": "fail",
                                "error": "read messages hashcodes was not provided",
                            }
                        )
                    )
                    return
                result, status = await self.read_messages(hashcodes)
                if result:
                    await self.send(
                        text_data=json.dumps(
                            {
                                "status": status,
                            }
                        )
                    )
                await self.send(
                    text_data=json.dumps(
                        {
                            "status": "fail",
                            "error": status,
                        }
                    )
                )
            # команда получения истории сообщений
            case "fetch_messages":
                try:
                    await self.fetch_messages_redis()
                except Exception as e:
                    # FIXME! залоггировать
                    await self.send(
                        text_data=json.dumps(
                            {
                                "status": "fail",
                                "error": e,
                            }
                        )
                    )
            # команда отправки нового сообщения
            case "new_message":
                if not text_data_json.get("message"):
                    await self.send(
                        text_data=json.dumps(
                            {"error": "no message was provided"}
                        )
                    )
                    return
                try:
                    await self.new_message(text_data_json.get("message"))
                except Exception as e:
                    # FIXME! залоггировать
                    await self.send(
                        text_data=json.dumps(
                            {
                                "status": "fail",
                                "error": e,
                            }
                        )
                    )
            # неизвестная команда
            case _:
                await self.send(
                    text_data=json.dumps(
                        {"status": "fail", "error": "unknown command provided"}
                    )
                )
