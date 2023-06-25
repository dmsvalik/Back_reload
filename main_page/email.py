from django.contrib.auth.tokens import default_token_generator
from djoser import email, utils
from djoser.conf import settings


EMAILS = {}


class Activation(email.ActivationEmail):
    """Email Activation Token Generator."""
    template_name = "email/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        uid, token = context['uid'], context['token']
        EMAILS[user.email] = {'uid': uid, 'token': token}
        return context


class Confirmation(email.ConfirmationEmail):
    template_name = "email/confirmation.html"
