from django.db import models

from app.main_page.models import UserAccount


class ChatModel(models.Model):
    # customer = models.ForeignKey(
    #     UserAccount, on_delete=models.SET_NULL, verbose_name='customer',
    #     related_name='executors_chat'
    # )
    # executor = models.ForeignKey(
    #     UserAccount, on_delete=models.SET_NULL, verbose_name='executor',
    #     related_name='customers_chat'
    # )
    participants = models.ManyToManyField(
        UserAccount,
        related_name='chats',
        verbose_name='Участники чата'
    )

    def last_10_messages(self):
        return self.messages.order_by('-timestamp').all()[:10]

    def __str__(self) -> str:
        return f'chat {self.pk}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class MessageModel(models.Model):
    """
    Модель сообщения чата. Указываются отправитель, время отправки и
    текст сообщения.
    """

    from_user = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        verbose_name='Отправитель',
        related_name='messages',
        db_index=True
    )
    to_chat = models.ForeignKey(
        ChatModel,
        on_delete=models.CASCADE,
        verbose_name='Чат',
        related_name='messages'
    )
    timestamp = models.DateTimeField(
        verbose_name='Время отправки',
        auto_now_add=True,
        editable=False,
        db_index=True
    )
    text_content = models.TextField(
        verbose_name='Текст сообщения'
    )

    def __str__(self):
        return f"{self.from_user.name}: {self.text_content[:20]}"

    # Meta
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('-timestamp',)
