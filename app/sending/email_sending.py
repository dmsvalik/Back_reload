from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from templated_mail.mail import BaseEmailMessage

from app.orders.models import OrderModel
from config.settings import SENDING


User = get_user_model()


class OrderEmail(BaseEmailMessage):
    template_name = "order_created.html"

    def get_context_data(self):
        """Получение данных для наполнения context для шаблона письма."""
        context = super().get_context_data()

        user_id = context.get("user_id")
        order_id = context.get("order_id")
        try:
            user = User.objects.get(id=user_id)
            order = OrderModel.objects.get(id=order_id)
            context["username"] = user.name
            context["order_name"] = order.name
            context["uid"] = utils.encode_uid(user.pk)
            context["token"] = default_token_generator.make_token(user)
            context["url"] = SENDING["DISABLE_URL"].format(**context)
            return context
        except Exception:
            return context
