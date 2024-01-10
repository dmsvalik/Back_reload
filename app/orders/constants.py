ORDER_STATE_CHOICES = (
    ("draft", "Черновик"),
    ("offer", "Создание предложений"),
    ("selected", "Исполнитель выбран"),
    ("completed", "Заказ выполнен"),
)


class ErrorMessages:
    QUESTION_ANSWER_REQUIRED = "Вопрос '{}' требует ответа."
    FILE_NOT_FOUNDED = "Файл не найден."
