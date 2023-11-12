<<<<<<< HEAD
=======
from drf_yasg.utils import swagger_auto_schema
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

<<<<<<< HEAD
from questionnaire.models import QuestionnaireType
from questionnaire.serializers import QuestionnaireTypeSerializer


=======
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
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104
@api_view(["GET"])
@permission_classes([AllowAny])
def get_questionnaire(request, questionnaire_id):
    questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
<<<<<<< HEAD
    serializer = QuestionnaireTypeSerializer(instance=questionnaire)
    return Response(serializer.data)
    # response = Response(serializer.data)
    # response.set_cookie("key", "qwertyuio")
    # if 'key' in request.COOKIES:
    #     print(request.COOKIES.get('key'))
    # return response
=======
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
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104
