from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from orders.models import OrderModel
from questionnaire.models import QuestionnaireType, Question
from questionnaire.permissions import IsOrderOwnerWithoutUser
from questionnaire.serializers import QuestionnaireTypeSerializer, \
    QuestionnaireShortTypeSerializer, QuestionnaireResponseSerializer
from questionnaire.swagger_documentation.questionnaire import \
    QuestionnaireGetList, QuestionnaireTypeGetList, QuestionnaireResponsePost
from utils import errorcode


@swagger_auto_schema(
    operation_description=QuestionnaireGetList.operation_description,
    request_body=QuestionnaireGetList.request_body,
    responses=QuestionnaireGetList.responses,
    method="GET"
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_questionnaire(request, questionnaire_id):
    try:
        questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
    except Exception:
        raise errorcode.QuestionnaireIdNotFound()
    key = request.COOKIES.get('key')
    serializer = QuestionnaireTypeSerializer(instance=questionnaire,
                                             context={"key": key})
    response = Response(serializer.data)
    if serializer.data and not OrderModel.objects.filter(key=key,
                                                         user_account__isnull=True).exists():
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


@swagger_auto_schema(
    operation_description=QuestionnaireResponsePost.operation_description,
    request_body=QuestionnaireResponsePost.request_body,
    responses=QuestionnaireResponsePost.responses,
    method="POST"
)
@api_view(["POST"])
@permission_classes([IsOrderOwnerWithoutUser])
def collect_answers(request, questionnaire_id):
    order = OrderModel.objects.get(key=request.COOKIES.get('key'))
    try:
        questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
    except Exception:
        raise errorcode.QuestionnaireIdNotFound()
    serializer = QuestionnaireResponseSerializer(data=request.data, many=True,
                                                 context={"order": order, "questionnaire": questionnaire})
    serializer.is_valid(raise_exception=True)
    questionnaire_questions = Question.objects.filter(
        chapter__type=questionnaire)
    questions_with_answers = [answer["question"] for answer in request.data]
    for question in questionnaire_questions:
        if question.answer_required and not question.option and question.id not in questions_with_answers:
            raise ValidationError({
                "question": f"Вопрос '{question.id}' требует ответа."
            })
        if (question.answer_required
                and question.option
                and question.id not in questions_with_answers
                and {"question": question.option.question.id,
                     "response": question.option.text} in request.data
        ):
            raise ValidationError({
                "question": f"Вопрос '{question.id}' требует ответа."
            })
    serializer.save(order=order)
    return Response(serializer.data)
