from datetime import datetime


from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.orders.models import OrderOffer
from .models import ChatMessage, Conversation


User = get_user_model()


@receiver(
    post_save,
    sender=OrderOffer,
    dispatch_uid="create_new_chat_and_first_message",
)
def manage_chats_for_offer(sender, instance, **kwargs):
    """Сигнал вызывается при изменении оффера"""
    if kwargs.get("created"):
        # если оффер создается, порождается чат,
        # где первым сообщений станет коммерческое предложение
        # из оффера
        try:
            contractor = instance.user_account
            new_conversation = Conversation.objects.create(
                client=instance.order_id.user_account,
                contractor=contractor,
                offer=instance,
            )
            ChatMessage.objects.create(
                conversation=new_conversation,
                sender=contractor,
                text=instance.offer_description,
                sent_at=datetime.now(),
            )
        except Exception as e:
            # FIXME! Залоггировать
            print("Shit happens", e)
    else:
        # если оффер редактируется, если его статус имеет значение
        # True, принудительно блокируются все чаты, относящиеся к этому заказу
        # кроме порожденного редактируемым оффером
        try:
            order = instance.order_id
            if instance.offer_status:
                offers_ids = (
                    OrderOffer.objects.filter(
                        order_id=order,
                    )
                    .exclude(pk=instance.pk)
                    .values_list("pk", flat=True)
                )
                chats = Conversation.objects.filter(
                    offer__in=offers_ids,
                )
                for chat in chats:
                    chat.is_blocked = True
                Conversation.objects.bulk_update(
                    chats,
                    ["is_blocked"],
                )
                if Conversation.objects.filter(
                    offer=instance,
                ).exists():
                    current_order_chat = Conversation.objects.filter(
                        offer=instance,
                    ).first()
                    current_order_chat.is_match = True
                    current_order_chat.save()

        except Exception as e:
            # FIXME! Залоггировать
            print("Shit happens", e)
