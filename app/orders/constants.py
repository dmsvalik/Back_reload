from enum import Enum


class OfferState(Enum):
    PROCESSE = "processed"
    VIEWED = "viewed"
    SELECTED = "selected"
    REJECTED = "rejected"


class OrderState(Enum):
    DRAFT = "draft"
    OFFER = "offer"
    SELECTED = "selected"
    COMPLETED = "completed"


OFFER_STATE_CHOICES = (
    (OfferState.PROCESSE.value, "В обработке"),  # при создании оффера
    (OfferState.VIEWED.value, "Просмотрен"),  # при просмотре оффера заказчиком
    (OfferState.SELECTED.value, "Выбран"),  # при выборе оффера
    (
        OfferState.REJECTED.value,
        "Отклонен",
    ),  # заказчик выбрал другой оффер к заказу
)

ORDER_STATE_CHOICES = (
    (OrderState.DRAFT.value, "Черновик"),
    (OrderState.OFFER.value, "Создание предложений"),
    (OrderState.SELECTED.value, "Исполнитель выбран"),
    (OrderState.COMPLETED.value, "Заказ выполнен"),
)


class ErrorMessages:
    QUESTION_ANSWER_REQUIRED = "Вопрос '{}' требует ответа."
    FILE_NOT_FOUNDED = "Файл не найден."
