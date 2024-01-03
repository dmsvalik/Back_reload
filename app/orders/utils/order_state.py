from app.orders.models import OrderModel, STATE_CHOICES
from app.questionnaire.models import QuestionResponse, Question
from app.utils.errorcode import OrderInWrongStatus, OrderAnswersNotComplete

from django.db.models import QuerySet, Prefetch

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
        if not self._is_draft():
            raise OrderInWrongStatus()

        if not self.answer_is_complete():
            raise OrderAnswersNotComplete()

        self.instance.state = STATE_CHOICES[1][0]
        self.instance.save()

    def answer_is_complete(self) -> bool:
        """
        Пробегает по каждому вопросу и смотрит что его массив ответов не пустой
        Если какой-то из массивов вопроса пуст возвращает False
        """
        questions: QuerySet[Question] = self._get_questions_by_order()
        for question in questions:
            if not question.answers:
                return False
        return True

    def _get_questions_by_order(self) -> QuerySet[Question]:
        """
        Возвращает все вопросы связанные с этим заказом, ответ на которые обязателен
        А так же подтягивает ответы связанные с этим заказом и ответами
        """
        question = (
            Question.objects.filter(
                chapter__type=self.instance.questionnaire_type,
                answer_required=True,
                option__isnull=True,
            )
            .prefetch_related(
                Prefetch(
                    lookup="questionresponse_set",
                    queryset=QuestionResponse.objects.filter(
                        order=self.instance
                    ).all(),
                    to_attr="answers",
                )
            )
            .all()
        )
        return question
