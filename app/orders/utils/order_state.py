from app.orders.models import OrderModel, STATE_CHOICES
from app.questionnaire.models import QuestionResponse
from app.utils.errorcode import OrderInWrongStatus, OrderAnswersNotComplete

from abc import ABC, abstractclassmethod


class OrderState(ABC):
    """
    Базовый класс для манипуляций со статусом заказа
    """

    DEFAULT_STATE: str = STATE_CHOICES[0][0]

    def __init__(self, instance: OrderModel):
        self.instance = instance

    @abstractclassmethod
    def execute(self):
        """
        Нужно реализовать у наследников
        Подразумевает изменение статуса заказа
        """
        ...

    def _is_draft(self) -> bool:
        if self.instance.state == self.DEFAULT_STATE:
            return True
        return False


class OrderStateActivate(OrderState):
    """
    Класс для активация заказа, меняет статус заказа на "offer"
    """

    def execute(self) -> None:
        self.answer_is_complete()
        if not self._is_draft():
            raise OrderInWrongStatus()

        if not self.answer_is_complete():
            raise OrderAnswersNotComplete()

        self.instance.state = STATE_CHOICES[1][0]
        self.instance.save()

    def answer_is_complete(self) -> bool:
        answer_set = (
            QuestionResponse.objects.filter(order=self.instance.pk)
            .select_related("question")
            .all()
        )
        for answer in answer_set:
            if answer.question.answer_required == False:
                return False
        return True
