from django.dispatch import Signal
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response

from app.users.models import UserAccount
from app.orders.models import OrderModel, OrderFileData, STATE_CHOICES
from app.users.utils.quota_manager import UserQuotaManager
from app.sending.views import send_user_notifications

post_request = Signal()


class AuthSignal:
    """
    Отвечает за вызов всех сигналов которые нужны для приложения users
    для реализации сигнала можно создать метод в этом классе и вызвать его
    в методе __call__, передавать в сигнал можно либо имеющиеся аргументы
    либо любые ключевы, которые попадут в kwargs
    """

    def __call__(
            self,
            request: Request,
            user: UserAccount,
            response: Response | None = None,
            addition: bool = False,
            notify: bool = False,
            **kwargs
            ):
        self._quota_recalcuate(request, addition, user, response)
        if notify:
            self._user_notify(user)

    def _quota_recalcuate(self, request: Request, addition: bool, user: UserAccount, response: Response):
        """
        Метод для запуска пересчета квоты пользователя после регистрации либо получения токена см. views.py
        При нахождении ключа "key" в куках удаляет его от туда,
        Если находят заказ по ключю, то присваеват его пользователя и меняет стаутс заказа
        Если находит файлы этого заказа вызывает менеджер для управления квотой пользователя
        для пересчета квоты
        """
        cookie_key: str = request.COOKIES.get("key")

        if cookie_key:
            order: OrderModel | None = OrderModel.objects.filter(key=cookie_key, user_account__isnull=True).first()
            response.delete_cookie("key")

            if order:
                OrderModel.objects.filter(pk=order.pk).update(
                    user_account=user,
                    state=STATE_CHOICES[1][0]
                )
                self.order = order

                files: QuerySet[OrderFileData] | None = OrderFileData.objects.filter(order_id__pk=order.pk).all()

                if files:
                    manager = UserQuotaManager(user)
                    if bool(addition):
                        manager.add_many(files=files)
                    else:
                        manager.subtract_many(files=files)



    def _user_notify(self, user: UserAccount):
        """
        Вызывает функицю для тправки уведомления юзеру
        Этот метод должен вызываеться в методе __call__
        После _quota_recalcuate, так как в том методе происхоит
        присваивание заказа атрибуту класса "self.order = order"
        """
        if hasattr(self, "order") and user.notifications:
            send_user_notifications(
            user,
            "ORDER_CREATE_CONFIRMATION",
            {"order_id": self.order.id,"user_id": user.id},
            [user.email]
            )

post_request.connect(AuthSignal())
