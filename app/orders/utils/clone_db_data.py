from django.contrib.auth import get_user_model

from app.orders.models import OrderModel, OrderFileData
from app.questionnaire.models import (
    QuestionResponse,
    QuestionnaireType,
    Question,
)
from app.users.utils.quota_manager import UserQuotaManager
from .servise import save_many_obj_to_db


class BaseOrderDB(object):
    pass


class CloneOrderDB(BaseOrderDB):
    """
    Класс с набором методов для клонирования информации
    """

    def __init__(
        self, user_id: int, old_order_id=None, new_order_id=None
    ) -> None:
        """
        Класс с набором методов для клонирования информации
        @param old_order_id: id копируемого заказа
        @param new_order_id: id нового заказа
        @param user_id: id пользователя
        """
        self.old_order_id = old_order_id
        self.user_id = user_id
        self.new_order_id = new_order_id

    def clone_order(self) -> int:
        """
        Метод копирует данные заказа.
        @return: id - нового заказа
        """
        if self.old_order_id is None:
            raise Exception("Не указан ID клонируемого заказа")
        old_order = OrderModel.objects.values(
            "name", "order_description", "questionnaire_type"
        ).get(pk=self.old_order_id)
        old_order["questionnaire_type"] = QuestionnaireType.objects.get(
            pk=old_order["questionnaire_type"]
        )
        user = get_user_model().objects.get(pk=self.user_id)
        new_order = OrderModel.objects.create(user_account=user, **old_order)
        new_order.save()
        self.new_order_id = new_order.pk
        return new_order.pk

    def clone_order_question_response(self) -> None:
        """
        Копирование ответов на вопросы анкеты
        @return:
        """
        responses = QuestionResponse.objects.filter(
            order_id=self.old_order_id
        ).values("response", "question_id")
        save_many_obj_to_db(
            QuestionResponse, responses, order_id=self.new_order_id
        )

    def clone_order_file_data(self) -> None:
        """
        Копирование информации о файлах в БД
        @return:
        """
        files_data = OrderFileData.objects.filter(
            order_id=self.old_order_id
        ).values(
            "question_id",
            "original_name",
            "yandex_path",
            "server_path",
            "yandex_size",
            "server_size",
        )
        new_order = OrderModel.objects.get(pk=self.new_order_id)
        for file in files_data:
            file["question_id"] = Question.objects.get(pk=file["question_id"])
        save_many_obj_to_db(OrderFileData, files_data, order_id=new_order)

    def update_order_file_data(self, path_to: str) -> None:
        """
        Метод обновляет пути до файлов в БД
        @param path_to: Новый путь до папки с файлами
        @return:
        """
        files = OrderFileData.objects.filter(order_id=self.new_order_id)
        user = get_user_model().objects.get(pk=self.user_id)
        quota_manager = UserQuotaManager(user)
        for file in files:
            file.yandex_path = f"{path_to}/{file.yandex_path.split('/')[-1]}"
            file.server_path = f"{path_to}/{file.server_path.split('/')[-1]}"
        OrderFileData.objects.bulk_update(
            files, ["yandex_path", "server_path"], batch_size=100
        )
        quota_manager.add_many(files)
