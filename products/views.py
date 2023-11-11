from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerializer


class CategoryAPIView(APIView):
    """
    ORDER. STEP 1. Получить список товаров для заказа и создания ответов по анкете.

    """

    permission_classes = [AllowAny]
    model = Category
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        result = Category.objects.all()
        return Response({"category_rooms": CategorySerializer(result, many=True).data})
