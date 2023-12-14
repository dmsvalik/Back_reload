from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Conversation(models.Model):
    """
    Модель чата.
    Объединяет участников и сообщения.
    Нейминг для избежания подмены понятий
    """
    client = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='заказчик',
        related_name='client_chats',
        null=True,
    )
    contractor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='исполнитель',
        related_name='contractor_chats',
        null=True,
    )
    is_match = models.BooleanField(
        verbose_name='случился ли match',
        default=False,
    )
    is_blocked = models.BooleanField(
        verbose_name='заблокирован ли чат',
        default=False,
    )

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'

    def __str__(self):
        return f'{self.client} - {self.contractor}'


class ChatMessage(models.Model):
    """
    Модель сообщения.
    Сообщение принадлежит конкретному чату
    и содержит ссылку на юзера.
    Желательно НЕ менять ордеринг
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        verbose_name='сообщение',
        related_name='messages',
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='отправитель',
        related_name='messages',
        null=True,
        blank=True,
    )
    text = models.TextField(
        verbose_name='текст',
    )
    sent_at = models.DateTimeField(
        verbose_name='Время отправки',
        editable=False,
    )

    class Meta:
        verbose_name = 'сообщение в чате'
        verbose_name_plural = 'сообщения в чатах'
        ordering = ('-sent_at',)

    def __str__(self):
        return self.text[:15]
