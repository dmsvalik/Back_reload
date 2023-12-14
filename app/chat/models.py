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




# from django.db import models
#
# from app.users.models import UserAccount
#
#
# class ChatModel(models.Model):
#     # customer = models.ForeignKey(
#     #     UserAccount, on_delete=models.SET_NULL, verbose_name='customer',
#     #     related_name='executors_chat'
#     # )
#     # executor = models.ForeignKey(
#     #     UserAccount, on_delete=models.SET_NULL, verbose_name='executor',
#     #     related_name='customers_chat'
#     # )
#     participants = models.ManyToManyField(
#         UserAccount,
#         related_name='chats',
#         verbose_name='Участники чата'
#     )
#
#     def last_10_messages(self):
#         return self.messages.order_by('-timestamp').all()[:10]
#
#     def __str__(self) -> str:
#         return f'chat {self.pk}'
#
#     class Meta:
#         verbose_name = 'Чат'
#         verbose_name_plural = 'Чаты'
#
#
# class MessageModel(models.Model):
#     """
#     Модель сообщения чата. Указываются отправитель, время отправки и
#     текст сообщения.
#     """
#
#     from_user = models.ForeignKey(
#         UserAccount,
#         on_delete=models.CASCADE,
#         verbose_name='Отправитель',
#         related_name='messages',
#         db_index=True
#     )
#     to_chat = models.ForeignKey(
#         ChatModel,
#         on_delete=models.CASCADE,
#         verbose_name='Чат',
#         related_name='messages'
#     )
#     timestamp = models.DateTimeField(
#         verbose_name='Время отправки',
#         auto_now_add=True,
#         editable=False,
#         db_index=True
#     )
#     text_content = models.TextField(
#         verbose_name='Текст сообщения'
#     )
#
#     def __str__(self):
#         return f"{self.from_user.name}: {self.text_content[:20]}"
#
#     # Meta
#     class Meta:
#         verbose_name = 'Сообщение'
#         verbose_name_plural = 'Сообщения'
#         ordering = ('-timestamp',)
