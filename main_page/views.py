from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import PersonalClientData
from .serializers import PersonalClientSerializer


class PersonalClientAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        Получить персональные данные пользователя (телефон, имя, адрес...)

        ---
        """
        pk = kwargs.get('pk', None)
        if not pk:
            p = PersonalClientData.objects.all()
            return Response({'personal_data': PersonalClientSerializer(p, many=True).data})
        else:
            p = PersonalClientData.objects.filter(pk=pk)
            return Response({'personal_data': PersonalClientSerializer(p, many=True).data})

    def post(self, request):
        """
        Сохранение персональных данных пользователя (телефон, имя, адрес...)

        ---
        - 'person_telephone': 89117861593
        - 'person_name': Sam
        - 'person_address': Rusia

        """

        username = request.user

        post_new = PersonalClientData.objects.create(
            user_account_id=username,
            person_telephone=request.data['person_telephone'],
            person_name=request.data['person_name'],
            person_address=request.data['person_address']
        )

        return Response({'personal_data': PersonalClientSerializer(post_new).data})

    def put(self, request, *args, **kwargs):
        """
        Изменение персональных данных пользователя (телефон, имя, адрес...)

        ---
        """
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = PersonalClientData.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = PersonalClientSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})
