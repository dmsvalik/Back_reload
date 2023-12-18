from django.conf import settings
from rest_framework import serializers

# from .models import ChatModel, MessageModel
from .models import ChatMessage, Conversation


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.email')

    class Meta:
        model = ChatMessage
        fields = ('id', 'sender', 'text', 'sent_at')
        read_only_fields = ('id', 'sender', 'sent_at')


class ChatSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField('get_messages')
    client = serializers.CharField(source='client.email')
    contractor = serializers.CharField(source='contractor.email')

    class Meta:
        model = Conversation
        fields = ('id', 'client', 'contractor', 'messages')

    def get_messages(self, instance):
        serializer = MessageSerializer(
            instance.messages.all()[:settings.CHATTING['LIST_MESSAGE_LIMIT']],
            many=True,
        )
        return serializer.data
