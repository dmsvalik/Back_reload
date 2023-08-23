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

        # проверяем наличие писем на сброс от пользователя
        check_user = EmailSendTime.objects.filter(email=user).order_by('id')
        time_now = datetime.now().hour * 60 + datetime.now().minute
        score = list()

        # собираем последние 3 записи (так как можно отправлять 3 записи в час)
        if len(check_user) >= 3:
            for item in check_user[len(check_user) - 3:]:
                score.append(item.timestamp.hour * 60 + item.timestamp.minute)

            result = time_now - score[0]
            if result <= 60:
                raise EmailTimestampError('We have already sent message to this email. Try 1 hour latter')

        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.USERNAME_RESET_CONFIRM_URL.format(**context)

        EmailSendTime.objects.create(email=user, api_call='reset_email')
        return context
