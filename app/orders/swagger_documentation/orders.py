from typing import List, Optional

from drf_yasg import openapi

from app.orders.serializers import AllOrdersClientSerializer, OrderOfferSerializer
from app.questionnaire.serializers import QuestionnaireResponseSerializer


def generate_400_response(fields: List[str]):
    default_value = openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(type=openapi.TYPE_STRING)
    )
    properties = {}
    for field in fields:
        properties[field] = default_value
    return openapi.Response("Bad Request", openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=properties
    ))


DEFAULT_RESPONSES = {
    204: openapi.Response("Success response"),
    401: openapi.Response(
        description="Unauthorized",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "detail": openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided.",
            }
        }
    ),
    403: openapi.Response("Forbidden", openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )),
    404: openapi.Response("Not Found", openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )),
    413: openapi.Response(
        description="Request Entity Too Large",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    ),
    500: openapi.Response(
        description="INTERNAL_SERVER_ERROR",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        examples={
            "application/json": {
                "detail": "Internal server error occurred.",
            }
        },
    )
}


class BaseSwaggerSchema:
    operation_description: str
    request_body: Optional[openapi.Schema]
    manual_parameters: Optional[List[openapi.Parameter]]
    responses: openapi.Responses


class OfferGetList(BaseSwaggerSchema):
    operation_description = "Вывод всех офферов к заказу."
    request_body = None
    responses = {
        200: openapi.Response("Success response", OrderOfferSerializer(many=True)),
        404: DEFAULT_RESPONSES[404]
    }


class OrderCreate(BaseSwaggerSchema):
    operation_description = "Создание заказа"
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['questionnaire_type_id', ],
        properties={
            'order_name': openapi.Schema(
                title='Название заказа',
                maxLength=150,
                type=openapi.TYPE_STRING,
            ),
            'order_description': openapi.Schema(
                title='Описание заказа',
                maxLength=300,
                type=openapi.TYPE_STRING
            ),
            'questionnaire_type_id': openapi.Schema(
                title='Связанная анкета',
                type=openapi.TYPE_INTEGER
            )
        })
    responses = {
        201: openapi.Response("Success response", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'success': openapi.Schema(default='the order was created', type=openapi.TYPE_STRING),
                'order_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            })),
        404: DEFAULT_RESPONSES[404]
    }


class OfferCreate(BaseSwaggerSchema):
    operation_description = "Cоздание оффера к заказу."
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['offer_price', 'offer_execution_time'],
        properties={
            'offer_price': openapi.Schema(
                title='Цена офера',
                maxLength=300,
                type=openapi.TYPE_STRING,
            ),
            'offer_execution_time': openapi.Schema(
                title='Время выполнения офера',
                maxLength=300,
                type=openapi.TYPE_STRING
            ),
            'offer_description': openapi.Schema(
                title='Описание офера',
                maxLength=300,
                type=openapi.TYPE_STRING
            )
        })
    responses = {
        201: openapi.Response("Success response", OrderOfferSerializer),
        400: generate_400_response(['offer_price', 'offer_execution_time', 'offer_description']),
        403: DEFAULT_RESPONSES[403],
        404: DEFAULT_RESPONSES[404],
    }


class AllOrdersClientGetList(BaseSwaggerSchema):
    operation_description = "Краткая информация обо всех заказах пользователя, кроме выполненных."
    request_body = None
    responses = {
        200: openapi.Response("Success response", AllOrdersClientSerializer(many=True)),
        401: DEFAULT_RESPONSES[401],
        403: DEFAULT_RESPONSES[403],
        500: DEFAULT_RESPONSES[500],
    }
    manual_parameters = [openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING)]


class ArchiveOrdersClientGetList(BaseSwaggerSchema):
    operation_description = "Краткая информация о выполненных заказах пользователя."
    request_body = None
    responses = {
        200: openapi.Response("Success response", AllOrdersClientSerializer(many=True)),
        401: DEFAULT_RESPONSES[401],
        403: DEFAULT_RESPONSES[403],
        500: DEFAULT_RESPONSES[500],
    }
    manual_parameters = [openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING)]


class FileOrderGet(BaseSwaggerSchema):
    operation_description = "Получение изображения и передача его на фронт."
    manual_parameters = [
        openapi.Parameter(
            "file_id",
            openapi.IN_PATH,
            description="ID записи файла в БД",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ]
    responses = {
        200: openapi.Response("Success response"),
        403: DEFAULT_RESPONSES[403],
        404: DEFAULT_RESPONSES[404],
        500: DEFAULT_RESPONSES[500],
    }


class UploadImageOrderPost(BaseSwaggerSchema):
    operation_description = "Загрузка изображения заказа."
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["order_id", "upload_file"],
        properties={
            "order_id": openapi.Schema(type=openapi.TYPE_STRING, description="ID заказа"),
            "upload_file": openapi.Schema(type=openapi.TYPE_FILE, description="Файл изображения для загрузки")
        }
    )
    responses = {
        202: openapi.Response(
            description="Accepted",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "task_id": openapi.Schema(type=openapi.TYPE_STRING, description="ID задачи обработки изображения")
                }
            )
        ),
        400: generate_400_response(["order_id", "upload_file"]),
        403: DEFAULT_RESPONSES[403],
        413: DEFAULT_RESPONSES[413],
    }


class QuestionnaireResponsePost(BaseSwaggerSchema):
    operation_description = "Отправка ответов на анкету."
    request_body = QuestionnaireResponseSerializer(many=True)
    responses = {
        201: openapi.Response("Success response", QuestionnaireResponseSerializer(many=True)),
        400: generate_400_response(["question"]),
        404: DEFAULT_RESPONSES[404]
    }


class QuestionnaireResponseGet(BaseSwaggerSchema):
    operation_description = "Получение ответов на анкету к заказу."
    request_body = None
    responses = {
        200: openapi.Response("Success response", QuestionnaireResponseSerializer(many=True)),
        403: DEFAULT_RESPONSES[403],
        404: DEFAULT_RESPONSES[404]
    }
