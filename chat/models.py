from django.contrib.auth.models import User
from django.db.models import (Model, TextField, DateTimeField, ForeignKey,
                              CASCADE)

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from main_page.models import UserAccount


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(UserAccount, related_name='chat_rooms')
    
    def __str__(self):
        return self.name


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False,
                              db_index=True)
    
    def __str__(self):
        return str(self.id)
    
    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def save(self, *args, **kwargs):
        """Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Удаление лишних пробелов
        super().save(*args, **kwargs)
        # Отправка уведомлений о новом сообщении
        if new is None:
            self.notify_ws_clients()

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'receive_group_message',
            'message': self.id
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{self.chat_room.id}",
            notification
        )


    # Meta
    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)
