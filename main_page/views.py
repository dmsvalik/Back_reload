from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import PersonalClientData
from .serializers import PersonalClientSerializer


class PersonalClientAPIView(APIView):

    def get(self, request):
        """
        Запрос на получение данных (телефон, имя, адрес...)

        ---
        :parameter
        - вернуться данные конкретно на пользователя токена JWT
        """
        p = PersonalClientData.objects.all()
        return Response({'personal_data': PersonalClientSerializer(p, many=True).data})

    def post(self, request):
        """
        Сохранение новых данных (телефон, имя, адрес...)

        ---
        - 'person_telephone': 89117861593
          required: true
          type: string

        - 'person_name': Sam
          required: true
          type: string

        - 'person_address': Rusia
          required: true
          type: string

        """

        username = request.user

        post_new = PersonalClientData.objects.create(
            user_account_id=username,
            person_telephone=request.data['person_telephone'],
            person_name=request.data['person_name'],
            person_address=request.data['person_address']
        )

        return Response({'personal_data': PersonalClientSerializer(post_new).data})
