from typing import List, Optional

from drf_yasg import openapi

from orders.serializers import OrderOfferSerializer


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
    ))
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
