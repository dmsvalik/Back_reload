from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import PersonalClientData
from .serializers import PersonalClientSerializer


class PersonalClientAPIView(APIView):
    def get(self, request):
        p = PersonalClientData.objects.all()
        return Response({'personal_data': PersonalClientSerializer(p, many=True).data})

    def post(self, request):
        username = request.user

        post_new = PersonalClientData.objects.create(
            user_account_id=username,
            person_telephone=request.data['person_telephone'],
            person_name=request.data['person_name'],
            person_address=request.data['person_address']
        )

        return Response({'personal_data': PersonalClientSerializer(post_new).data})
