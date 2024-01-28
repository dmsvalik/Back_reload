import datetime

from django.dispatch import Signal
from django.db.models import QuerySet
from django.db.models.signals import post_save

from app.users.models import UserAccount, UserQuota, UserAgreement
from app.orders.constants import ORDER_STATE_CHOICES as STATE_CHOICES
from app.orders.models import OrderModel, OrderFileData
from app.users.utils.quota_manager import UserQuotaManager
from app.sending.views import send_user_notifications

quota_recalculate = Signal()
send_notify = Signal()


class QuotaRecalculateSignal:
    """
    Запускает сигнал для пересчета квоты
    Если заказ не передан - сигнал не отрабатывает
    :user - обьект пользователя
    :order - обьект заказа
    :change_order_state - флаг на то следует ли изменять статус заказа

    """

    def __call__(
        self,
        user: UserAccount,
        order: OrderModel,
        change_order_state: bool = False,
        **kwargs
    ):
        if not order:
            return

        self._update_order(order, user, change_order_state)

        files: QuerySet[OrderFileData] | None = OrderFileData.objects.filter(
            order_id__pk=order.pk
        ).all()

        if files:
            manager = UserQuotaManager(user)
            manager.add_many(files=files)

    def _update_order(
        self, order: OrderModel, user: UserAccount, change_state: bool = False
    ):
        """
        Обновляет заказ, присваивает заказу пользователя
        и при положительном знаении change_state - меняет статус
        """
        update_data = {"user_account": user}
        if change_state:
            update_data.update({"state": STATE_CHOICES[1][0]})
        OrderModel.objects.filter(pk=order.pk).update(**update_data)


class SendNotifySignal:
    """
    Запускает сигнал для отправки уведомления пользователю
    Если заказ не передан - сигнал не отработает
    """

    def __call__(self, user: UserAccount, order: OrderModel, **kwargs):
        if not order:
            return
        self._send_notify(user, order)

    def _send_notify(self, user, order):
        send_user_notifications(
            user,
            "ORDER_CREATE_CONFIRMATION",
            {"order_id": order.id, "user_id": user.id},
            [user.email],
        )


quota_recalculate.connect(QuotaRecalculateSignal())
send_notify.connect(SendNotifySignal())


def create_userquota_and_agreement(sender, instance, created, **kwargs):
    """
    Создание объекта уведомления пользователя по email
    при создании пользователя.
    """
    if created:
        UserQuota.objects.create(user=instance)
        UserAgreement.objects.create(
            user_account=instance, date=datetime.date.today()
        )


post_save.connect(create_userquota_and_agreement, sender=UserAccount)
