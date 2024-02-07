from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from templated_mail.mail import BaseEmailMessage

from app.orders.models import OrderModel
from app.questionnaire.models import (
    QuestionnaireChapter,
    QuestionnaireType,
)
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
        """Получение данных для наполнения context для шаблона письма.
        Заказ оформлен и отправлен исполнителям.
        """
        context = super().get_context_data()

        order_id = context.get("order_id")
        try:
            order = OrderModel.objects.get(id=order_id)
            context["order_name"] = order.name
            return context
        except Exception:
            return context


class QuestionnaireEmail(BaseLinkEmail):
    template_name = "questionnaire_created.html"

    def get_context_data(self):
        """Получение данных для наполнения context для шаблона письма анкеты.
        Уведомление что анкета заполнена.
        """
        context = super().get_context_data()

        questionnaire_id = context.get("questionnaire_id")
        chapter_id = context.get("chapter_id")
        try:
            questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
            chapter = QuestionnaireChapter.objects.get(id=chapter_id)
            # Добавление данных в контекст
            context["questionnaire_type"] = questionnaire.type
            context["chapter_name"] = chapter.name
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


class ConstructorEmail(BaseLinkEmail):
    template_name = "constructor_created.html"

    def get_context_data(self):
        """Получение данных для наполнения context для шаблона письма.
        Уведомление  исполнителей о  новых заказах.
        """
        context = super().get_context_data()

        order_id = context.get("order_id")
        # Здесь будет исполнитель
        try:
            order = OrderModel.objects.get(id=order_id)
            context["order_name"] = order.name
            # Здесь будет исполнитель
            return context
        except Exception:
            return context
