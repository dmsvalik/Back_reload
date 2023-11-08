from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from orders.models import OrderModel
from questionnaire.models import QuestionnaireType
from questionnaire.serializers import QuestionnaireTypeSerializer, QuestionnaireShortTypeSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def get_questionnaire(request, questionnaire_id):
    questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
    serializer = QuestionnaireTypeSerializer(instance=questionnaire)
    response = Response(serializer.data)
    if serializer.data:
        order = OrderModel.objects.create(
            user_account=None,
            name=f"Заказ №{1 if not OrderModel.objects.last() else OrderModel.objects.last().id + 1}",
            card_category=questionnaire.category.category,
        )
        response.set_cookie("key", order.key)
    # return Response(serializer.data)
    if 'key' in request.COOKIES:
        print(request.COOKIES.get('key'))
    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def get_questionnaire_types(request, category_id):
    questionnaires = QuestionnaireType.objects.filter(category=category_id)
    serializer = QuestionnaireShortTypeSerializer(questionnaires, many=True)
    return Response(serializer.data)
