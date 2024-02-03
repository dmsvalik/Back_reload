from typing import List, Optional

from drf_yasg import openapi

from app.orders.serializers import (
    AllOrdersClientSerializer,
    OrderOfferSerializer,
)
from app.questionnaire.serializers import (
    QuestionnaireResponseSerializer,
    OrderFullSerializer,
    FileSerializer,
)
from app.orders.serializers import OrderModelSerializer
from config.settings import SWAGGER_TAGS, MAX_STORAGE_QUOTA


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
    operation_description: str
    request_body: Optional[openapi.Schema]
    manual_parameters: Optional[List[openapi.Parameter]]
    responses: openapi.Responses


class OfferGetList(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("order"), SWAGGER_TAGS.get("offer")]
    operation_id = "order-create"
    operation_summary = "Вывод всех офферов к заказу."
    operation_description = (
        "Используйте этот метод для получения списка всех офферов к заказу.\n"
        "**Ограничения:**\n\n"
        "- Доступ только для авторизованного пользователя\n"
    )
    manual_parameters = [
        openapi.Parameter(
            type=openapi.TYPE_INTEGER,
            name="id",
            description="ID заказа",
            in_=openapi.IN_PATH,
        )
    ]
    request_body = None
    responses = {
        200: openapi.Response(
            "Success response", OrderOfferSerializer(many=True)
        ),
        404: DEFAULT_RESPONSES[404],
    }


class OrderCreate(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("order")]
    operation_id = "order-create"
    operation_summary = "Создание заказа"
    operation_description = (
        "Используйтие этот общедоступный метод для создания нового заказa.\n"
        "Если пользователь "
        "авторизован, то становится владельцем заказа. В противном случае в "
        "куки получает уникальный ключ для идентификации после регистрации.\n"
        " В случае успешного создания заказа, пользователь получит на "
        "указанный ранее email письмо с параметрами заказа"
    )
    method = "POST"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[
            "questionnaire_type_id",
        ],
        properties={
            "order_name": openapi.Schema(
                title="Название заказа",
                maxLength=150,
                type=openapi.TYPE_STRING,
            ),
            "order_description": openapi.Schema(
                title="Описание заказа",
                maxLength=300,
                type=openapi.TYPE_STRING,
            ),
            "questionnaire_type_id": openapi.Schema(
                title="Связанная анкета", type=openapi.TYPE_INTEGER
            ),
        },
    )
    responses = {
        201: openapi.Response(
            "Success response",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "success": openapi.Schema(
                        default="the order was created",
                        type=openapi.TYPE_STRING,
                    ),
                    "order_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                },
            ),
        ),
        404: DEFAULT_RESPONSES[404],
    }


class OfferCreate(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("order"), SWAGGER_TAGS.get("offer")]
    operation_summary = "Создание оффера к заказу"
    operation_description = (
        "Используйте этот метод для создания оффера к заказу.\n"
        "**Ограничения:**\n\n"
        "- Доступ только для **авторизованного пользователя**\n"
        "- Доступ только для **исполнителя**"
    )
    manual_parameters = [
        openapi.Parameter(
            type=openapi.TYPE_INTEGER,
            name="id",
            description="ID заказа",
            in_=openapi.IN_PATH,
        )
    ]
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["offer_price", "offer_execution_time"],
        properties={
            "offer_price": openapi.Schema(
                title="Цена офера",
                maxLength=300,
                type=openapi.TYPE_STRING,
            ),
            "offer_execution_time": openapi.Schema(
                title="Время выполнения офера",
                maxLength=300,
                type=openapi.TYPE_STRING,
            ),
            "offer_description": openapi.Schema(
                title="Описание офера", maxLength=300, type=openapi.TYPE_STRING
            ),
        },
    )
    responses = {
        201: openapi.Response("Success response", OrderOfferSerializer),
        400: generate_400_response(
            ["offer_price", "offer_execution_time", "offer_description"]
        ),
        403: DEFAULT_RESPONSES[403],
        404: DEFAULT_RESPONSES[404],
    }


class AllOrdersClientGetList(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("order"), SWAGGER_TAGS.get("users_service")]
    operation_summary = "Список активных заказов авторизованного пользователя"
    operation_description = (
        "Используйте этот метод для получения списка краткой информации обо "
        "всех заказах пользователя, кроме "
        "выполненных.\n\n**Ограничения:**\n"
        "- Доступ только для **авторизованного пользователя**\n"
    )
    request_body = None
    responses = {
        200: openapi.Response(
            "Success response", AllOrdersClientSerializer(many=True)
        ),
        401: DEFAULT_RESPONSES[401],
        403: DEFAULT_RESPONSES[403],
        500: DEFAULT_RESPONSES[500],
    }


class OrderStateActivateSwagger(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("order")]
    operation_summary = "Активация заказа"
    request_body = None
    responses = {
        200: openapi.Response("Success response", schema=OrderModelSerializer),
        401: DEFAULT_RESPONSES[401],
        403: DEFAULT_RESPONSES[403],
        500: DEFAULT_RESPONSES[500],
    }


class ArchiveOrdersClientGetList(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("order"), SWAGGER_TAGS.get("users_service")]
    operation_summary = (
        "Список завершенных заказов авторизованного пользователя"
    )
    operation_description = (
        "Используйте этот метод для получения списка завершенных заказов "
        "авторизованного пользователя"
        "\n\n**Ограничения:**\n"
        "- Доступ только для **авторизованного пользователя**\n"
    )
    request_body = None
    responses = {
        200: openapi.Response(
            "Success response", AllOrdersClientSerializer(many=True)
        ),
        401: DEFAULT_RESPONSES[401],
        403: DEFAULT_RESPONSES[403],
        500: DEFAULT_RESPONSES[500],
    }
    manual_parameters = [
        openapi.Parameter(
            "Authorization", in_=openapi.IN_HEADER, type=openapi.TYPE_STRING
        )
    ]


class FileOrderDelete(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("files")]
    operation_id = "delete-file-order"
    operation_summary = "Удаление файла из Yandex"
    operation_description = (
        "Удаление файла из Yandex.Cloud.\nПроверяется наличие записи о файле,"
        " после удаляется сам файл и связанные с ним элементы (превью и "
        "запись в бд).\n**При наличии файла возвращается ID CeleryTask**\n"
        "\n\n**Ограничения:**\n\n1. Проверка пользователя(или):\n-- Владелец"
        "\n-- Файл без владельца"
    )
    method = "DELETE"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[
            "file_id",
        ],
        properties={
            "file_id": openapi.Schema(
                title="Id файла",
                type=openapi.TYPE_INTEGER,
            )
        },
    )
    responses = {
        204: openapi.Response(
            "Success response",
        ),
        404: DEFAULT_RESPONSES[404],
        500: DEFAULT_RESPONSES[500],
    }


class QuestionnaireResponsePost(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("order"), SWAGGER_TAGS.get("questionnaire")]
    operation_id = "post-order-answers"
    operation_summary = "Отправка ответов на анкету к заказу"
    operation_description = (
        "Используйте этот метод для отправки ответов на анкету заказа."
        "\n\n**Ограничения:**\n"
        "- Авторизованный пользователь является **владельцем заказа**\n"
        "- В куках неавторизованного пользователя **содержится уникальный "
        "ключ**"
    )
    method = "POST"
    request_body = QuestionnaireResponseSerializer(many=True)
    manual_parameters = [
        openapi.Parameter(
            type=openapi.TYPE_INTEGER,
            name="id",
            description="ID заказа",
            in_=openapi.IN_PATH,
        )
    ]
    responses = {
        201: openapi.Response(
            "Success response", QuestionnaireResponseSerializer(many=True)
        ),
        400: generate_400_response(["question"]),
        404: DEFAULT_RESPONSES[404],
    }


class QuestionnaireResponseGet(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("order"), SWAGGER_TAGS.get("questionnaire")]
    operation_id = "get-order-answers"
    operation_summary = "Получение ответов на вопросы анкеты к заказу"
    operation_description = (
        "Используйте этот метод для получения ответов на вопросы  для анкеты "
        "к заказу."
        "\n\n**Ограничения:**\n"
        "- Авторизованный пользователь является **владельцем заказа**\n"
        "- В куках неавторизованного пользователя **содержится уникальный "
        "ключ**"
    )
    manual_parameters = [
        openapi.Parameter(
            type=openapi.TYPE_INTEGER,
            name="id",
            description="ID заказа",
            in_=openapi.IN_PATH,
        )
    ]
    request_body = None
    responses = {
        200: openapi.Response("Success response", OrderFullSerializer()),
        403: DEFAULT_RESPONSES[403],
        404: DEFAULT_RESPONSES[404],
    }


class OrderUpdate(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("order")]
    operation_id = "update-order"
    operation_summary = "Обновление информации о заказе"
    operation_description = (
        "Используйте этот метод для обновления информации о заказе."
        "\n\n**Ограничения:**\n"
        "- Авторизованный пользователь является **владельцем заказа**\n"
        "- В куках неавторизованного пользователя **содержится уникальный "
        "ключ**"
    )
    manual_parameters = [
        openapi.Parameter(
            type=openapi.TYPE_INTEGER,
            name="id",
            description="ID заказа",
            in_=openapi.IN_PATH,
        )
    ]
    request_body = OrderFullSerializer()
    responses = {
        200: openapi.Response("Success response", OrderFullSerializer()),
        403: DEFAULT_RESPONSES[403],
        404: DEFAULT_RESPONSES[404],
    }


class QuestionnaireResponseLastGet(BaseSwaggerSchema):
    tags = [
        SWAGGER_TAGS.get("order"),
    ]
    operation_id = "get-last-order-answers"
    operation_summary = (
        "Получение ответов на вопросов анкеты к последнему заказу в "
        "статусе черновик."
    )
    operation_description = (
        "Используйте этот метод для получения ответов на вопросов анкеты к "
        "последнему заказу в статусе черновик."
        "\n\n**Ограничения:**\n"
        "- Авторизованный пользователь является \n"
    )
    method = "GET"
    request_body = None
    responses = {
        200: openapi.Response("Success response", OrderFullSerializer()),
        403: DEFAULT_RESPONSES[403],
        404: DEFAULT_RESPONSES[404],
    }


class AttachFileAnswerPost(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("files")]
    operation_id = "file attach"
    operation_summary = "Загрузка документа к ответу"
    operation_description = (
        "Добавление файла к определенному вопросу заказа.\n**(Общий объем "
        "данных пользователя не должен превышать установленную квоту в разме"
        f"ре {MAX_STORAGE_QUOTA / 1024 / 1024} mb.)**\n\n"
        "**Входные данные:**\n"
        "- pk:int (обязательное) - id заказа к которому крепится файл,"
        "\n- Данные которые передаются через form-data:"
        "\n-- question_id: int (обязательное) - id вопроса к которому"
        "прилагается файл или изображение,"
        "\n-- upload_file (обязательное) - файл или изображение, отправляемые"
        "пользователем, передается через request.FILES"
        "**\n\n**Ограничения:**\n"
        "1. Проверка пользователя:\n-- Владелец\n 2. Формат файлов:\n"
        '--"image/jpg"\n--"image/gif"\n--"image/jpeg"\n--'
        '"application/pdf"'
    )
    method = "POST"
    manual_parameters = [
        openapi.Parameter(
            "upload_file",
            openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description="Upload file",
        ),
        openapi.Parameter(
            "question_id",
            openapi.IN_FORM,
            type=openapi.TYPE_INTEGER,
            required=True,
            description="ID вопроса",
        ),
    ]
    responses = {
        201: FileSerializer(),
        400: generate_400_response(["question_id", "upload_file"]),
        403: DEFAULT_RESPONSES[403],
    }


class FileOrderDownload(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("files")]
    operation_id = "file-order-download"
    operation_summary = "Получение прямой ссылки на скачивание файла"
    operation_description = (
        "Эндпоинт принимает id файла в БД и **делает редирект по прямой "
        " ссылке на скачивание файла с ЯндексCloud.**\n\n**Ограничения:**\n\n"
        "1. Доступно всем пользователям."
    )
    method = "GET"
    responses = {
        302: openapi.Response(
            "Success response. Redirect to download file",
        ),
        401: openapi.Response("Unauthorized"),
        404: openapi.Response("FileNotFound"),
    }


class OrderOfferRetrieve(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("offer")]
    operation_summary = (
        "Получение информации о отдельном оффере " "**в разработке**"
    )
    deprecated = True


class OrderOfferDelete(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("offer")]
    operation_summary = "Удаление отдельного оффера **в разработке**"
    deprecated = True


class OrderOfferUpdate(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("offer")]
    operation_summary = "Изменение отдельного оффера **в разработке"
    deprecated = True


class CloneOrderCreate(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("order")]
    operation_summary = "Пересоздание заказа"
    operation_description = (
        "Используйте этот метод для создания нового заказа на основе "
        "созданного ранее.\nПри использовании данного метода скопируются все "
        "параметры предыдущего заказа (анкеты, файлы, описание и название)."
        "**\n\n**Ограничения:**\n\n"
        "1. Проверка авторизован ли пользователь\n"
        "2. Проверка на существование заказа с переданным id\n"
        "3. Проверка пользователя(или):\n"
        "-- Владелец заказа\n"
        "4. Проверка наличия доступного дискового пространства для "
        "пользователя"
    )
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[
            "order_id",
        ],
        properties={
            "order_id": openapi.Schema(
                title="ID заказа для клонирования",
                type=openapi.TYPE_INTEGER,
            )
        },
    )
    responses = {
        201: openapi.Response(
            "Success response",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "new_order_id": openapi.Schema(
                        type=openapi.TYPE_INTEGER, title="ID нового заказа"
                    ),
                },
            ),
        ),
        401: DEFAULT_RESPONSES[401],
        403: DEFAULT_RESPONSES[403],
        500: DEFAULT_RESPONSES[500],
    }
