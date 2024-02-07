from django.conf import settings
from rest_framework import serializers

from .models import ChatMessage, Conversation
from .utils import RedisClient


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.email")

    class Meta:
        model = ChatMessage
        fields = ("id", "sender", "text", "sent_at", "is_read", "hashcode")
        read_only_fields = ("id", "sender", "sent_at", "is_read", "hashcode")


class ChatIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ("id",)


class ChatSerializer(ChatIDSerializer):
    messages = serializers.SerializerMethodField("get_messages")
    client = serializers.CharField(source="client.email")
    contractor = serializers.CharField(source="contractor.email")
    unread_messages = serializers.SerializerMethodField("get_unread_count")

    class Meta(ChatIDSerializer.Meta):
        fields = ChatIDSerializer.Meta.fields + (
            "client",
            "contractor",
            "messages",
            "unread_messages",
        )

    def get_messages(self, instance):
        serializer = MessageSerializer(
            instance.messages.all()[: settings.CHATTING["LIST_MESSAGE_LIMIT"]],
            many=True,
        )
        return serializer.data

    def get_unread_count(self, instance):
        redis = RedisClient.from_settings()
        chat_keys = redis.search_by_pattern(f"chat_{instance.pk}*")
        unread_count = 0
        for key in chat_keys:
            message = redis.get_message_by_key(key)
            if message.get("is_read") and message.get("is_read") == "False":
                unread_count += 1
        try:
            not_read_in_db = ChatMessage.objects.filter(
                is_read=False
            ).values_list("hashcode", flat=True)
            for code in not_read_in_db:
                if code not in chat_keys:
                    unread_count += 1
        except:
            # FIXME! проверить и потом о убрать try/catch
            pass

        return unread_count
