from rest_framework import status
from typing import List, Optional
from drf_yasg import openapi
from config.settings import SWAGGER_TAGS
from app.main_page.error_message import error_responses


class BaseSwaggerSchema:
    operation_description: str
    request_body: Optional[openapi.Schema]
    manual_parameters: Optional[List[openapi.Parameter]]
    responses: openapi.Responses


class ContractorAgreementCreate(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("contractor")]
    operation_summary = "Создание соглашения с исполнителем."
    operation_description = "Создание соглашения с исполнителем."
    responses = {
        status.HTTP_400_BAD_REQUEST: error_responses[
            status.HTTP_400_BAD_REQUEST
        ],
        status.HTTP_401_UNAUTHORIZED: error_responses[
            status.HTTP_401_UNAUTHORIZED
        ],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ],
    }


class SupportRetrieve(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("support")]
    operation_summary = "Задать вопрос в поддержку"
    operation_description = "Задать вопрос в поддержку"
    responses = {
        status.HTTP_401_UNAUTHORIZED: error_responses[
            status.HTTP_401_UNAUTHORIZED
        ],
        status.HTTP_404_NOT_FOUND: error_responses[status.HTTP_404_NOT_FOUND],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ],
    }


class SupportCreate(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("support")]
    operation_summary = "Создание вопроса в поддержку"
    operation_description = "Создание вопроса в поддержку"
    responses = {
        status.HTTP_400_BAD_REQUEST: error_responses[
            status.HTTP_400_BAD_REQUEST
        ],
        status.HTTP_401_UNAUTHORIZED: error_responses[
            status.HTTP_401_UNAUTHORIZED
        ],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ],
    }


class SupportDelete(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("support")]
    operation_summary = "Удаление конкретного вопроса"
    operation_description = "Удаление конкретного вопроса"
    responses = {
        status.HTTP_204_NO_CONTENT: error_responses[
            status.HTTP_204_NO_CONTENT
        ],
        status.HTTP_401_UNAUTHORIZED: error_responses[
            status.HTTP_401_UNAUTHORIZED
        ],
        status.HTTP_404_NOT_FOUND: error_responses[status.HTTP_404_NOT_FOUND],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ],
    }


class SupportList(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("support")]
    operation_summary = "Получить список созданных вопросов и ответов"
    operation_description = "Получить список созданных вопросов и ответов"
    responses = {
        status.HTTP_401_UNAUTHORIZED: error_responses[
            status.HTTP_401_UNAUTHORIZED
        ],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ],
    }


class CooperationCreate(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("support"), SWAGGER_TAGS.get("contractor")]
    operation_summary = "Создание запроса на сотрудничество"
    operation_description = "Создание запроса на сотрудничество"
    responses = {
        status.HTTP_400_BAD_REQUEST: error_responses[
            status.HTTP_400_BAD_REQUEST
        ],
        status.HTTP_401_UNAUTHORIZED: error_responses[
            status.HTTP_401_UNAUTHORIZED
        ],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ],
    }


class CooperationList(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("support"), SWAGGER_TAGS.get("contractor")]
    operation_summary = "Получить список запросов на сотрудничество"
    operation_description = "Получить список запросов на сотрудничество"
    responses = {
        status.HTTP_401_UNAUTHORIZED: error_responses[
            status.HTTP_401_UNAUTHORIZED
        ],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ],
    }


class CooperationDelete(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("support"), SWAGGER_TAGS.get("contractor")]
    operation_summary = "Удаление запроса на сотрудничество"
    operation_description = "Удаление запроса на сотрудничество"
    responses = {
        status.HTTP_204_NO_CONTENT: error_responses[
            status.HTTP_204_NO_CONTENT
        ],
        status.HTTP_401_UNAUTHORIZED: error_responses[
            status.HTTP_401_UNAUTHORIZED
        ],
        status.HTTP_404_NOT_FOUND: error_responses[status.HTTP_404_NOT_FOUND],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ],
    }


class CooperationDetail(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("support"), SWAGGER_TAGS.get("contractor")]
    operation_summary = "Получить запрос на сотрудничество"
    operation_description = "Получить запрос на сотрудничество"
    responses = {
        status.HTTP_401_UNAUTHORIZED: error_responses[
            status.HTTP_401_UNAUTHORIZED
        ],
        status.HTTP_404_NOT_FOUND: error_responses[status.HTTP_404_NOT_FOUND],
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses[
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ],
    }
