from typing import List, Optional

from drf_yasg import openapi

from config.settings import SWAGGER_TAGS


def generate_400_response(fields: List[str]):
    default_value = openapi.Schema(
        type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
    )
    properties = {}
    for field in fields:
        properties[field] = default_value
    return openapi.Response(
        "Bad Request",
        openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties),
    )


DEFAULT_RESPONSES = {
    204: openapi.Response("Success response"),
    401: openapi.Response(
        description="Unauthorized",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided.",
            }
        },
    ),
    403: openapi.Response(
        "Forbidden",
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    ),
    404: openapi.Response(
        "Not Found",
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    ),
    413: openapi.Response(
        description="Request Entity Too Large",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    ),
    500: openapi.Response(
        description="INTERNAL_SERVER_ERROR",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        examples={
            "application/json": {
                "detail": "Internal server error occurred.",
            }
        },
    ),
}


class BaseSwaggerSchema:
    tags: List[str]
    operation_summary: str
    operation_description: str
    request_body: Optional[openapi.Schema]
    manual_parameters: Optional[List[openapi.Parameter]]
    responses: openapi.Responses


class AllDelete(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("service")]
    operation_id = "delete"
    operation_summary = "Очистка базы данных"
    operation_description = (
        "Используйте этот метод для полной очистки базы данных. База данных "
        "будет очищена полностью кроме записи админа\n"
        "**Ограничения**\n\n- Администратор\n**Использование метода крайне "
        "опасно, так как полностью очищает базу данных**"
    )
    method = "delete"
    request_body = None
    responses = {
        202: openapi.Response("Success response"),
        404: DEFAULT_RESPONSES[404],
        500: DEFAULT_RESPONSES[500],
    }


class DocsView(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("files")]
    operation_summary = "Редирект на превью картинки"
    operation_id = "document-view"
    operation_description = (
        "Редирект на превью картинки, с добавлением ограничений доступа."
        "\n\n**Ограничения:**\n\n"
        "1. Проверка на существование файла\n2. Проверка пользователя(или):\n"
        "-- Администратор\n-- Владелец\n-- Исполнитель"
    )
    method = "get"
    manual_parameters = [
        openapi.Parameter(
            "path",
            openapi.IN_PATH,
            description="Путь до файла",
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ]
    responses = {
        202: openapi.Response("Success response"),
        401: openapi.Response("Unauthorized"),
        404: openapi.Response("FileNotFound"),
    }


class CreateAdmin(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("service")]
    operation_id = "create_admin"
    operation_summary = "Создание пользователя с правами администратора"
    operation_description = (
        "Используйте этот метод для создания "
        "пользователя с правами администратора"
    )
    method = "post"
    request_body = None
    responses = {
        202: openapi.Response("Success response"),
        404: DEFAULT_RESPONSES[404],
        500: DEFAULT_RESPONSES[500],
    }


class CreateAllData(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("service")]
    operation_id = "create_all_data"
    operation_summary = "Создание тестового наполнения базы данных"
    operation_description = (
        "Используйте этот метод для тестового наполнения базы данных"
    )
    method = "post"
    request_body = None
    responses = {
        202: openapi.Response("Success response"),
        404: DEFAULT_RESPONSES[404],
        500: DEFAULT_RESPONSES[500],
    }


class CheckExpAuctionOrdersDocs(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("contractor")]
    operation_summary = "Проверка заказов в статусе аукциона"
    operation_description = (
        "Используйте этот метод для проверки заказов в статусе аукциона"
    )
    method = "get"


class GalleryImagesList(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("service")]
    operation_summary = " Отображение картинок на главной странице"
    operation_description = (
        "Отображение картинок на главной странице в слайдерах"
    )


class GetTaskStatus(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("service")]
    operation_summary = "Получение результата отложенной задачи"
    operation_description = (
        "Используйте этот метод для получения статуса выполнения отложенной "
        "задачи. В случае успешного выполнения задачи, в ответе так-же "
        "вернется и сам результат выполнения."
    )
    method = "get"
