import os

from django.contrib.auth import get_user_model

from app.orders.models import OrderModel, OrderFileData
from app.questionnaire.models import (
    QuestionResponse,
    QuestionnaireType,
    Question,
)
from .services import save_many_obj_to_db
from ...users.utils.quota_manager import UserQuotaManager


class BaseOrderDB(object):
    def __init__(self, user_id: int = None, order_id: int = None):
        """
        Базовый класс для работы с базой данных заказа
        @param order_id: id заказа
        @param user_id: id пользователя
        """
        self.user_id = user_id
        self.order_id = order_id

    def update_order_file_path(
        self, path_to: str, server: bool = True, cloud: bool = True
    ) -> None:
        """
        Метод обновляет пути до файлов в БД, по умолчанию обновляются все
        пути (сервер, YandexCloud), однако опционально можно отключить.
        @param path_to: Новый путь до папки с файлами
        @param server: bool флаг хранилища сервера
        @param cloud: bool флаг YandexCloud
        @return: QuerySet обновленных файлов
        """
        files = OrderFileData.objects.filter(order_id=self.order_id)

        fields_update = []
        if server:
            fields_update.append("server_path")
            files = files.exclude(server_path="")
        if cloud:
            fields_update.append("yandex_path")
            files = files.exclude(yandex_path="")

        for file in files:
            if server:
                file.server_path = os.path.join(
                    path_to, file.server_path.split("/")[-1]
                )
            if cloud:
                file.yandex_path = os.path.join(
                    path_to, file.yandex_path.split("/")[-1]
                )

        OrderFileData.objects.bulk_update(files, fields_update, batch_size=100)

        user = get_user_model().objects.get(pk=self.user_id)
        quota_manager = UserQuotaManager(user)
        quota_manager.add_many(files, server=server, cloud=cloud)


class CloneOrderDB(BaseOrderDB):
    """
    Класс с набором методов для клонирования информации
    """

    def __init__(self, user_id: int, old_order_id=None, order_id=None) -> None:
        """
        Класс с набором методов для клонирования информации
        @param old_order_id: id копируемого заказа
        @param order_id: id нового заказа
        @param user_id: id пользователя
        """
        super().__init__(user_id=user_id, order_id=order_id)
        self.old_order_id = old_order_id

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
        self.order_id = new_order.pk
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
            QuestionResponse, responses, order_id=self.order_id
        )

    def clone_order_file_data(self) -> bool:
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
        new_order = OrderModel.objects.get(pk=self.order_id)
        if not files_data:
            return False
        for file in files_data:
            file["question_id"] = Question.objects.get(pk=file["question_id"])
        save_many_obj_to_db(OrderFileData, files_data, order_id=new_order)
        return True


class UpdateOrderDB(BaseOrderDB):
    """
    Класс для обновления данных заказа в БД
    """

    def __init__(self, user_id: int, order_id: int = None) -> None:
        super().__init__(user_id=user_id, order_id=order_id)
