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
    if kwargs.get("created"):
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
        try:
            order = instance.order_id
            if instance.offer_status:
                # client = order.user_account
                # offers_users_ids = (
                offers_ids = (
                    OrderOffer.objects.filter(
                        order_id=order,
                    )
                    .exclude(pk=instance.pk)
                    .values_list("pk", flat=True)
                )
                chats = Conversation.objects.filter(
                    # client=client,
                    # contractor__in=offers_users_ids,
                    offer__in=offers_ids,
                )
                for chat in chats:
                    chat.is_blocked = True
                Conversation.objects.bulk_update(
                    chats,
                    ["is_blocked"],
                )
                if Conversation.objects.filter(
                    # client=client,
                    # contractor=instance.user_account,
                    offer=instance,
                ).exists():
                    current_order_chat = Conversation.objects.filter(
                        # client=client,
                        # contractor=instance.user_account,
                        offer=instance,
                    ).first()
                    current_order_chat.is_match = True
                    current_order_chat.save()

        except Exception as e:
            # FIXME! Залоггировать
            print("Shit happens", e)
