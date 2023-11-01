from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from questionnaire.models import QuestionnaireType
from questionnaire.serializers import QuestionnaireTypeSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def get_questionnaire(request, questionnaire_id):
    questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
    serializer = QuestionnaireTypeSerializer(instance=questionnaire)
    return Response(serializer.data)
