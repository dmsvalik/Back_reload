from djoser import email
from django.contrib.auth.tokens import default_token_generator
from .models import EmailSendTime

from djoser import utils
from djoser.conf import settings
from datetime import datetime

from .exceptions import EmailTimestampError


class Activation(email.ActivationEmail):
    template_name = "email/activation.html"


class Confirmation(email.ConfirmationEmail):
    template_name = "email/confirmation.html"


class UsernameReset(email.UsernameResetEmail):
    """ Отправка письма при сбросе почты - таймаут 3 часа """

    template_name = "email/username_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")

        # ищем по почте последний запрос и высчитываем в секундах с текущем временем
        check_user = EmailSendTime.objects.filter(email=user).latest('timestamp')
        check_time = datetime.now().replace(tzinfo=None) - check_user.timestamp.replace(tzinfo=None)
        check_seconds = check_time.total_seconds()
        if check_seconds < 20:
            raise EmailTimestampError('We have already sent message to this email. Try letter')

        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.USERNAME_RESET_CONFIRM_URL.format(**context)

        EmailSendTime.objects.create(email=user, api_call='reset_email')
        return context
