class ErrorMessages:
    RETRY_USERNAME_RESET_ERROR = (
        "We have already sent message to this email. Try 1 hour latter."
    )
    PHONE_FIELD_VALIDATION_ERROR = (
        "Телефон должен начинаться с +7, иметь 12 знаков(цифры)."
    )
    INVALID_CHARACTERS = "Недопустимые символы!"


class ModelChoices:
    ROLES_CHOICES = [("contractor", "Исполнитель"), ("client", "Заказчик")]


class EmailThemes:
    ACTIVATION_CONFIRMATION = "Подтверждение активации аккаунта."
    ACTIVATION = "Письмо активации аккаунта."
    RESET_EMAIL = "Письмо на сброс почты."
