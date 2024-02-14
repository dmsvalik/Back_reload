from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from templated_mail.mail import BaseEmailMessage

from app.orders.models import OrderModel

from config.settings import SENDING


User = get_user_model()


class BaseLinkEmail(BaseEmailMessage):
    """Базовый класс получения ссылки на отписку"""

    def get_context_data(self):
        context = super().get_context_data()

        user_id = context.get("user_id")

        try:
            user = User.objects.get(id=user_id)
            context["username"] = user.name
            context["uid"] = utils.encode_uid(user.pk)
            context["token"] = default_token_generator.make_token(user)
            context["url"] = SENDING["DISABLE_URL"].format(**context)
            return context
        except Exception:
            return context


class OrderEmail(BaseLinkEmail):
    template_name = "order_created.html"

    def get_context_data(self):
        """
        Получение данных для наполнения context для шаблона письма.
        Уведомление заказчика об оформлении заказа.
        """
        context = super().get_context_data()

        order_id = context.get("order_id")
        try:
            order = OrderModel.objects.get(id=order_id)
            context["order_name"] = order.name
            return context
        except Exception:
            return context


class ConstructorEmail(BaseLinkEmail):
    template_name = "constructor_notification.html"

    def get_context_data(self):
        """Получение данных для наполнения context для шаблона письма.
        Уведомление  исполнителей о  новых заказах.
        """
        context = super().get_context_data()

        order_id = context.get("order_id")
        try:
            order = OrderModel.objects.get(id=order_id)
            context["order_name"] = order.name
            return context
        except Exception:
            return context


class NewOfferEmail(BaseLinkEmail):
    template_name = "new_offer.html"

    def get_context_data(self):
        """
        Получение данных для наполнения context для шаблона письма.
        Оповещение заказчика о новых предложениях.
        """
        context = super().get_context_data()

        order_id = context.get("order_id")
        # offer_id = context.get("offer_id") - уточнить пункт (название)
        try:
            order = OrderModel.objects.get(id=order_id)
            # offer = OfferModel.objects.get(id=offer_id) - уточнить будущую модель
            context["order_name"] = order.name
            # context["offer_name"] = offer.name - уточнить
            return context
        except Exception:
            return context


class ChoiseConstructorEmail(BaseLinkEmail):
    template_name = "choise_constructor.html"

    def get_context_data(self):
        """Получение данных для наполнения context для шаблона письма анкеты.
        Уведомление что выбран Исполнитель.
        """
        context = super().get_context_data()

        order_id = context.get("order_id")
        try:
            order = OrderModel.objects.get(id=order_id)
            context["order_name"] = order.name
            return context
        except Exception:
            return context


class NoOfferConstructorEmail(BaseLinkEmail):
    template_name = "no_offer_constructor.html"

    def get_context_data(self):
        """Получение данных для наполнения context для шаблона письма анкеты.
        Уведомление что Исполнитель не сделал предложение.
        """
        context = super().get_context_data()

        order_id = context.get("order_id")
        try:
            order = OrderModel.objects.get(id=order_id)
            context["order_name"] = order.name
            return context
        except Exception:
            return context


class OpenChatOrderEmail(BaseLinkEmail):
    template_name = "open_chat.html"

    def get_context_data(self):
        """Получение данных для наполнения context для шаблона письма анкеты.
        Уведомление что Заказчик открыл чат с Исполнителем.
        """
        context = super().get_context_data()

        order_id = context.get("order_id")
        try:
            order = OrderModel.objects.get(id=order_id)
            context["order_name"] = order.name
            return context
        except Exception:
            return context


class CloseOrderWithConstructorEmail(BaseLinkEmail):
    template_name = "close_order_with_constructor.html"

    def get_context_data(self):
        """Получение данных для наполнения context для шаблона письма анкеты.
        Уведомление Исполнителя что Заказчик его выбрал.
        """
        context = super().get_context_data()

        order_id = context.get("order_id")
        try:
            order = OrderModel.objects.get(id=order_id)
            context["order_name"] = order.name
            return context
        except Exception:
            return context


class CloseOrderWithoutConstructorEmail(BaseLinkEmail):
    template_name = "close_order_without_constructor.html"

    def get_context_data(self):
        """Получение данных для наполнения context для шаблона письма анкеты.
        Уведомление Исполнителя что Заказчик его не выбрал.
        """
        context = super().get_context_data()

        order_id = context.get("order_id")
        try:
            order = OrderModel.objects.get(id=order_id)
            context["order_name"] = order.name
            return context
        except Exception:
            return context
