from templated_mail.mail import BaseEmailMessage


class OrderEmail(BaseEmailMessage):
    template_name = "order_created.html"

    # def get_context_data(self):
    #     # ActivationEmail can be deleted
    #     context = super().get_context_data()
    #
    #     user = context.get("user")
    #     context["uid"] = utils.encode_uid(user.pk)
    #     context["token"] = default_token_generator.make_token(user)
    #     context["url"] = settings.ACTIVATION_URL.format(**context)
    #     return context
