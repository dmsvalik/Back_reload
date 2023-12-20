from django.dispatch import Signal
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response

from app.users.models import UserAccount
from app.orders.models import OrderModel, OrderFileData, STATE_CHOICES
from app.users.utils import UserQuotaManager
from app.sending.views import send_user_notifications

post_request = Signal()


class AuthSignal:

    def __call__(self, **kwargs):
        request: Request = kwargs.get("request")
        addition: bool = bool(kwargs.get("addition", False))
        response: Response = kwargs.get("response")
        user: UserAccount = kwargs.get("user")
        notify: bool = bool(kwargs.get("notify", False))

        self._quota_recalcuate(request, addition, user, response)
        if notify:
            self._user_notify(user)

    def _quota_recalcuate(self, request: Request, addition: bool, user: UserAccount, response: Response):
        cookie_key: str = request.COOKIES.get("key")

        if cookie_key:
            order: OrderModel | None = OrderModel.objects.filter(key=cookie_key, user_account__isnull=True).first()

            if order:
                OrderModel.objects.filter(pk=order.pk).update(
                    user_account=user,
                    state=STATE_CHOICES[1][0]
                )
                self.order = order
                response.delete_cookie("key")

                files: QuerySet[OrderFileData] | None = OrderFileData.objects.filter(order_id__pk=order.pk).all()

                if files:
                    manager = UserQuotaManager(user)
                    if bool(addition):
                        manager.add_many(files=files)
                    else:
                        manager.subtract_many(files=files)



    def _user_notify(self, user: UserAccount):
        if hasattr(self, "order") and user.notifications:
            send_user_notifications(
            user,
            "ORDER_CREATE_CONFIRMATION",
            {"order_id": self.order.id,"user_id": user.id},
            [user.email]
            )

post_request.connect(AuthSignal())
