ORDER_STATE_CHOICES = (
    ("draft", "Черновик"),
    ("offer", "Создание предложений"),
    ("selected", "Исполнитель выбран"),
    ("completed", "Заказ выполнен"),
)

OFFER_STATE_CHOICES = (
    ("processed", "В обработке"),  # при создании оффера
    ("viewed", "Просмотрен"),  # при просмотре оффера заказчиком
    ("selected", "Выбран"),  # при выборе оффера
    ("rejected", "Отклонен"),  # заказчик выбрал другой оффер к заказу
    ("archive", "В архиве"),  # оффер перенесен в архив
)


class ErrorMessages:
    QUESTION_ANSWER_REQUIRED = "Вопрос '{}' требует ответа."
    FILE_NOT_FOUNDED = "Файл не найден."
