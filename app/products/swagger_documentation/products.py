from typing import List, Optional

from drf_yasg import openapi

from app.products.serializers import QuestionnaireShortTypeSerializer
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
    operation_description: str
    request_body: Optional[openapi.Schema]
    manual_parameters: Optional[List[openapi.Parameter]]
    responses: openapi.Responses


class QuestionnaireTypeGetList(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("questionnaire")]
    operation_summary = "Получение всех анкет категории"
    operation_description = "Получение всех анкет категории."
    request_body = None
    method = "GET"
    responses = {
        200: openapi.Response(
            "Success response", QuestionnaireShortTypeSerializer()
        ),
        404: DEFAULT_RESPONSES[404],
    }


class CategoryList(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("questionnaire")]
    operation_summary = "Получение списка категорий"
    operation_description = "Получение списка категорий"
