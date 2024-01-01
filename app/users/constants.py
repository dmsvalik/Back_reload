class ErrorMessages:
    RETRY_USERNAME_RESET_ERROR = (
        "We have already sent message to this email. Try 1 hour latter."
    )
    PHONE_FIELD_VALIDATION_ERROR = (
        "Телефон должен начинаться с +7, иметь 12 знаков(цифры)."
    )
    WRONG_NUMBER_OF_LETTER = (
        "Количество букв должно быть не менее 2 и не более 50."
    )
    INVALID_CHARACTERS = "Недопустимые символы!"


class ModelChoices:
    ROLES_CHOICES = [("contractor", "Исполнитель"), ("client", "Заказчик")]
