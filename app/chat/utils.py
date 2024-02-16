from datetime import datetime, timedelta, timezone
import hashlib

from asgiref.sync import sync_to_async

from django.contrib.auth import get_user_model
from django.db import transaction
from django.conf import settings

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from app.users.models import UserAccount
from .models import ChatMessage, Conversation
from .redis_client import RedisClient


User = get_user_model()


def generate_message_hash(message: dict):
    """Генерация хеша для сообщения"""
    str_for_hash = message["text"] + message["sent_at"]
    return hashlib.sha256(str_for_hash.encode()).hexdigest()


def store_messages_to_db(chat, hashcodes: list[str]):
    """
    Функция сброса данных из редиса в бд
    Получит все сообщения из редиски по хешкодам,
    соберет список, сбросит в бд и удалит из редиса
    """
    redis = RedisClient.from_settings()
    chat_messages = []
    keys_for_deletion = []
    chat_id = int(chat.split("_")[1])
    for code in hashcodes:
        message = redis.get_message(chat, code)
        is_read = False
        if message.get("is_read") and message.get("is_read") == "True":
            is_read = True
        chat_messages.append(
            ChatMessage(
                conversation=Conversation.objects.filter(pk=chat_id).first(),
                sender=UserAccount.objects.filter(
                    email=message["sender"]
                ).first(),
                text=message["text"],
                sent_at=message["sent_at"],
                is_read=is_read,
                hashcode=code,
            )
        )

        # подготовка к удалению
        keys_for_deletion.append(chat + ":" + code)

    with transaction.atomic():
        ChatMessage.objects.bulk_create(
            chat_messages,
        )
        success = True

    if success:
        redis.delete(keys_for_deletion)


def create_periodic_task():
    """
    Создание периодической задачи в celery beat
    Должно стартовать вместе с джангой при импорте приложения
    чатов
    """
    schedule, create = IntervalSchedule.objects.get_or_create(
        every=settings.CHATTING.get("REDIS_DB_STORE_PERIOD", 1),
        period=IntervalSchedule.MINUTES,
    )
    if not PeriodicTask.objects.filter(
        name="sync_chats_in_redis_and_db"
    ).exists():
        PeriodicTask.objects.create(
            name="sync_chats_in_redis_and_db",
            task="app.chat.tasks.store_chat_messages_from_redis_to_db",
            interval=schedule,
            start_time=datetime.now(timezone.utc) + timedelta(minutes=1),
        )


def load_message_history_to_redis(
    client: RedisClient, chat_id: int, offset: int = None, limit: int = None
):
    """
    Функция загрузки истории сообщений в редис из базы.
    Сейчас должна вызывать при создании Консюмера.
    При возникновении лагов вероятно следует доработать консюмер,
    чтобы вызывать обновлении истории порционно
    """
    chat = Conversation.objects.filter(pk=chat_id)
    if chat.exists() is False:
        return

    messages = ChatMessage.objects.filter(conversation=chat.first())[
        offset:limit
    ]

    for message in messages:
        client.store_message(
            "chat_" + str(chat_id),
            message.hashcode,
            {
                "text": message.text,
                "sender": str(message.sender),
                "sent_at": str(message.sent_at),
                "is_read": str(message.is_read),
            },
        )


async def async_load_message_history_to_redis(
    client: RedisClient, chat_id: int, offset: int = None, limit: int = None
):
    """
    То же что и выше, но асинхронное.
    """
    chat = Conversation.objects.filter(pk=chat_id)
    if chat.aexists() is False:
        return

    chat = await chat.afirst()

    messages = ChatMessage.objects.select_related("sender").filter(
        conversation=chat
    )
    messages = messages[offset:limit]

    async for message in messages:
        key = message.hashcode
        data = {
            "text": message.text,
            "sender": str(message.sender),
            "sent_at": str(message.sent_at),
            "is_read": str(message.is_read),
        }
        await sync_to_async(client.store_message)(
            "chat_" + str(chat_id),
            key,
            data,
        )
