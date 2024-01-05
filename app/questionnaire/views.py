from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from app.questionnaire.models import QuestionnaireType
from app.questionnaire.serializers import QuestionnaireTypeSerializer
from app.questionnaire.swagger_documentation.questionnaire import (
    QuestionnaireGetList,
)
from app.utils import errorcode


@swagger_auto_schema(
    operation_description=QuestionnaireGetList.operation_description,
    request_body=QuestionnaireGetList.request_body,
    responses=QuestionnaireGetList.responses,
    method="GET",
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_questionnaire(request, questionnaire_id: int):
    """
    Получение всех разделов, вопросов и вариантов ответов анкеты.
    URL: http://localhost/questionnaire/<int:questionnaire_id>/
    METHOD - "GET"
    questionnaire_id:int (обязательное) - id типа анкеты,
    """
    try:
        questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
    except Exception:
        raise errorcode.QuestionnaireIdNotFound()
    serializer = QuestionnaireTypeSerializer(instance=questionnaire)
    return Response(serializer.data)
