from celery import shared_task

from .redis_client import RedisClient
from .models import ChatMessage, Conversation
from app.users.models import UserAccount


@shared_task()
def store_chat_messages_from_redis_to_db():
    redis = RedisClient.from_settings()
    messages_in_redis = redis.search_by_pattern("chat*")
    message_for_db = []
    for key in messages_in_redis:
        # отвратительно, но это потому что ключик выглядит как
        # 'chat_1:a9bc510010352...
        id_and_code = key.split("_")[1].split(":")
        chat_id = id_and_code[0]
        code = id_and_code[1]
        message = redis.get_message_by_key(key)
        is_read = False
        if message.get("is_read") and message.get("is_read") is True:
            is_read = True
        message_for_db.append(
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

    ChatMessage.objects.bulk_create(
        message_for_db,
    )

    redis.delete(messages_in_redis)
