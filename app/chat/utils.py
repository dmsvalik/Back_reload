from datetime import datetime, timedelta, timezone
import hashlib

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from app.users.models import UserAccount
from .models import ChatMessage, Conversation
from .redis_client import RedisClient


def generate_message_hash(message: dict):
    str_for_hash = message["text"] + message["sent_at"]
    return hashlib.sha256(str_for_hash.encode()).hexdigest()


def store_messages_to_db(chat, hashcodes: list[str]):
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

    ChatMessage.objects.bulk_create(
        chat_messages,
    )

    redis.delete(keys_for_deletion)


def create_periodic_task():
    schedule, create = IntervalSchedule.objects.get_or_create(
        every=1, period=IntervalSchedule.MINUTES
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
