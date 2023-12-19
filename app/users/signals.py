from django.dispatch import Signal
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response

from app.users.models import UserAccount
from app.orders.models import OrderModel, OrderFileData
from app.users.utils import UserQuotaManager


post_request = Signal()


def quota_recalculate(**kwargs):
    """
    Пересчитывает квоту пользователя и удаляет ключ из куки
    При условии что есть ключ, найден заказ по ключю, найдены файлы у заказа
    Если в вызов сигнала передать ключ "addition" то менеджер будет прибавлять
    найденные размеры файла, если ключа нет то отнимать
    """
    request: Request = kwargs.get("sender")
    cookie_key: str = request.COOKIES.get("key")
    user: UserAccount = kwargs.get("user")

    if cookie_key:
        order: OrderModel | None = OrderModel.objects.filter(key=cookie_key, user_account__isnull=True).first()

        if order:
            order.user_account = user
            order.save()
            files: QuerySet[OrderFileData] | None = OrderFileData.objects.filter(order_id__pk=order.pk).all()

            if files:
                manager = UserQuotaManager(user)
                if bool(kwargs.get("addition", False)):
                    manager.add_many(files=files)
                else:
                    manager.subtract_many(files=files)

                response: Response = kwargs.get("reponse")
                response.delete_cookie("key")


post_request.connect(quota_recalculate)
