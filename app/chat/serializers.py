from rest_framework import serializers

# from .models import ChatModel, MessageModel
from .models import ChatMessage, Conversation


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'sender', 'text', 'sent_at')
        read_only_fields = ('id', 'sender', 'sent_at')


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'client', 'contractor', 'messages')
