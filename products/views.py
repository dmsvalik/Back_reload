# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from .models import CardModel
from .serializers import CardModelSerializer


class CardModelAPIView(APIView):
    """
    ORDER. STEP 1. Получить список товаров для заказа и создания ответов по анкете.

    """

    permission_classes = [AllowAny]
    model = CardModel
    serializer_class = CardModelSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        result = CardModel.objects.all()
        return Response({"card_rooms": CardModelSerializer(result, many=True).data})
