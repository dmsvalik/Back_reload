from djoser import email
from django.contrib.auth.tokens import default_token_generator

from config.settings import DJOSER_EMAIL_CLASSES
from .constants import ErrorMessages

from djoser import utils
from djoser.conf import settings
from datetime import datetime, timezone, timedelta

from app.users.exceptions import EmailTimestampError
from app.sending.models import SentNotification


class Activation(email.ActivationEmail):
    """Отправка письма активации."""

    template_name = "email/activation.html"


class Confirmation(email.ConfirmationEmail):
    """Отправка письма подтверждения активации."""

    template_name = "email/confirmation.html"


class UsernameReset(email.UsernameResetEmail):
    """Отправка письма при сбросе почты - таймаут 3 часа"""

    template_name = "email/username_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")

        # проверяем наличие писем на сброс от пользователя
        check_user = SentNotification.objects.filter(
            user=user, theme=DJOSER_EMAIL_CLASSES["USERNAME_RESET"]["theme"]
        ).order_by("id")
        time_now = datetime.now(tz=timezone.utc)
        score = list()

        # собираем последние 3 записи (так как можно отправлять 3 записи в час)
        if len(check_user) >= 3:
            for item in check_user[len(check_user) - 3 :]:
                score.append(item.created_at)

            result = time_now - score[0]
            if result <= timedelta(minutes=60):
                raise EmailTimestampError(
                    ErrorMessages.RETRY_USERNAME_RESET_ERROR
                )

        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.USERNAME_RESET_CONFIRM_URL.format(**context)

        SentNotification.objects.create(
            user=user,
            theme=DJOSER_EMAIL_CLASSES["USERNAME_RESET"]["theme"],
            type="email",
        )
        return context
