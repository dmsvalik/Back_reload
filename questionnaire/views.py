from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from orders.models import OrderModel
from questionnaire.models import QuestionnaireType
from questionnaire.serializers import QuestionnaireTypeSerializer, QuestionnaireShortTypeSerializer
from questionnaire.swagger_documentation.questionnaire import \
    QuestionnaireGetList, QuestionnaireTypeGetList


@swagger_auto_schema(
        operation_description=QuestionnaireGetList.operation_description,
        request_body=QuestionnaireGetList.request_body,
        responses=QuestionnaireGetList.responses,
        method="GET"
    )
@api_view(["GET"])
@permission_classes([AllowAny])
def get_questionnaire(request, questionnaire_id):
    questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
    key = request.COOKIES.get('key')
    serializer = QuestionnaireTypeSerializer(instance=questionnaire, context={"key": key})
    response = Response(serializer.data)
    if serializer.data and not OrderModel.objects.filter(key=key, user_account__isnull=True).exists():
        order = OrderModel.objects.create(
            user_account=None,
            name=f"Заказ №{1 if not OrderModel.objects.last() else OrderModel.objects.last().id + 1}",
            card_category=questionnaire.category.category,
        )
        response.set_cookie("key", order.key)
    return response

@swagger_auto_schema(
        operation_description=QuestionnaireTypeGetList.operation_description,
        request_body=QuestionnaireTypeGetList.request_body,
        responses=QuestionnaireTypeGetList.responses,
        method="GET"
    )
@api_view(["GET"])
@permission_classes([AllowAny])
def get_questionnaire_types(request, category_id):
    questionnaires = QuestionnaireType.objects.filter(category=category_id)
    serializer = QuestionnaireShortTypeSerializer(questionnaires, many=True)
    return Response(serializer.data)
