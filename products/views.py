from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ResponseModel
from .models import (CardModel, CategoryModel, QuestionsProductsModel)
from orders.serializers import OrderModelSerializer

from .serializers import (AnswerCreateSerializer, CardModelSerializer,
                          CategoryModelSeializer, QuestionModelSerializer)


class CardModelAPIView(APIView):
    """
    ORDER. STEP 1. Получить список комнат - кухня, спалья и т.д.

    """

    permission_classes = [IsAuthenticated]
    model = CardModel
    serializer_class = CardModelSerializer

    def get(self, request):

        """перед началом шагов по созданию заказа надо удалить старые ответы (без связки с заказом) """
        ResponseModel.objects.filter(user_account=request.user.id, order_id=None).delete()

        result = CardModel.objects.all()
        return Response({"card_rooms": CardModelSerializer(result, many=True).data})


class CategoryModelListAPIView(ListAPIView):
    """
    ORDER. STEP 2. Получить список категорий (возможных товаров) по id карточки (раздела)

    """

    model = CategoryModel
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSeializer

    def get_queryset(self):
        card_id = self.kwargs["card_id"]
        return CategoryModel.objects.filter(card__id=card_id).all()


class QuestionsModelListAPIView(ListAPIView):
    """
    ORDER. STEP 3.1. Получить список вопросов по id категории (товара)

    """

    model = QuestionsProductsModel
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionModelSerializer

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return QuestionsProductsModel.objects.filter(category__id=category_id).all()


class AnswerListAPIView(CreateAPIView):
    """
    ORDER. STEP 3.2. Создать ответы на вопросы

    """

    permission_classes = [IsAuthenticated]
    serializer_class = AnswerCreateSerializer

    def get_serializer(self, *args, **kwargs):
        """if an array is passed, set serializer to many"""
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(AnswerListAPIView, self).get_serializer(*args, **kwargs)


@api_view(['POST'])
def CreateOrderAnswers(request):
    """
    ORDER. STEP 4. Получить описание, сразу создать заказ (статус: Не закончен) и добавить все ответы без order_id.

    """

    # создаем заказ и передаем данные
    serializer = OrderModelSerializer(data=request.data, context={'request': request, 'state': 'new'})
    if serializer.is_valid():
        order_create = serializer.save()

        # если заказ создан, ищем ответы на вопросы (которые без привязки order_id) и записываем их к этому заказу
        ResponseModel.objects.filter(user_account=request.user.id, order_id=None).update(order_id=order_create.id)

        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
