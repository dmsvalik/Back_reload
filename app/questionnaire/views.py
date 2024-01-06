from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from app.questionnaire.models import QuestionnaireType
from app.questionnaire.serializers import QuestionnaireTypeSerializer
from app.questionnaire.swagger_documentation import questionnaire as swagger
from app.utils import errorcode


@swagger_auto_schema(**swagger.QuestionnaireGetList.__dict__)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_questionnaire(request, questionnaire_id):
    try:
        questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
    except Exception:
        raise errorcode.QuestionnaireIdNotFound()
    serializer = QuestionnaireTypeSerializer(instance=questionnaire)
    return Response(serializer.data)


# @swagger_auto_schema(
#     operation_description=QuestionnaireTypeGetList.operation_description,
#     request_body=QuestionnaireTypeGetList.request_body,
#     responses=QuestionnaireTypeGetList.responses,
#     method="GET"
# )
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def get_questionnaire_types(request, category_id):
#     questionnaires = QuestionnaireType.objects.filter(category=category_id)
#     serializer = QuestionnaireShortTypeSerializer(questionnaires, many=True)
#     return Response(serializer.data)


# @swagger_auto_schema(
#     operation_description=QuestionnaireResponsePost.operation_description,
#     request_body=QuestionnaireResponsePost.request_body,
#     responses=QuestionnaireResponsePost.responses,
#     method="POST"
# )
# @api_view(["POST"])
# @permission_classes([IsOrderOwnerWithoutUser])
# def collect_answers(request, questionnaire_id):
#     order = OrderModel.objects.get(key=request.COOKIES.get('key'))
#     try:
#         questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
#     except Exception:
#         raise errorcode.QuestionnaireIdNotFound()
#     serializer = QuestionnaireResponseSerializer(data=request.data, many=True,
#                                                  context={"order": order, "questionnaire": questionnaire})
#     serializer.is_valid(raise_exception=True)
#     questionnaire_questions = Question.objects.filter(
#         chapter__type=questionnaire)
#     questions_id_with_answers = [answer["question"] for answer in request.data]
#     questions_with_answers = Question.objects.filter(id__in=questions_id_with_answers).all()
#     for question in questionnaire_questions:
#         if question.answer_required and not question.option and question not in questions_with_answers:
#             raise ValidationError({
#                 "question": f"Вопрос '{question.id}' требует ответа."
#             })
#         if (question.answer_required
#                 and question.option
#                 and question not in questions_with_answers
#                 and {"question": question.option.question.id,
#                      "response": question.option.text} in request.data
#         ):
#             raise ValidationError({
#                 "question": f"Вопрос '{question.id}' требует ответа."
#             })
#     for question in questions_with_answers:
#         if question.option and question.option.question not in questions_with_answers:
#             raise ValidationError({
#                 "question": f"Вопрос '{question.option.question.id}' требует ответа."
#             })
#     serializer.save(order=order)
#     return Response(serializer.data)
