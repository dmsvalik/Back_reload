from typing import Optional, List

from drf_yasg import openapi

from app.file.serializers import FileModelSerializer
from app.orders.swagger_documentation.orders import DEFAULT_RESPONSES
from config.settings import SWAGGER_TAGS


class BaseSwaggerSchema:
    operation_description: str
    request_body: Optional[openapi.Schema]
    manual_parameters: Optional[List[openapi.Parameter]]
    responses: openapi.Responses


class UploadFile(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("files")]
    operation_summary = "Загрузка файлов"
    operation_description = "jgbcfybt"
    request_body = FileModelSerializer
    manual_parameters = [
        openapi.Parameter(
            "upload_file",
            openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description="Upload file",
        ),
    ]
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
