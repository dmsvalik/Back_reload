from rest_framework import serializers

from .models import ChatModel, MessageModel


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = ('id', 'from_user', 'text_content', 'timestamp')
        read_only_fields = ('id', 'timestamp')


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatModel
        fields = ('id', 'messages', 'participants')
        read_only_fields = ('id', 'messages')
