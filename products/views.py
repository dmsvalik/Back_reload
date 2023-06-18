from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (CardModel, CategoryModel, ProductModel,
                     QuestionsProductsModel)
from .serializers import (AnswerCreateSerializer, CardModelSerializer,
                          CategoryModelSeializer, ProductModelSerializer,
                          QuestionModelSerializer)


class CardModelAPIView(APIView):
    """
    Получить список комнат - кухня, спалья и т.д.

    """

    permission_classes = [AllowAny]
    model = CardModel
    serializer_class = CardModelSerializer

    def get(self, request):
        result = CardModel.objects.all()
        return Response({"card rooms": CardModelSerializer(result, many=True).data})


class CategoryModelListAPIView(ListAPIView):
    """
    Получить список категорий по id карточки

    """

    model = CategoryModel
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSeializer

    def get_queryset(self):
        card_id = self.kwargs["card_id"]
        return CategoryModel.objects.filter(card__id=card_id).all()


class ProductModelCreateAPIView(CreateAPIView):
    """
    Создать продукт заказа

    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProductModelSerializer


class ProductModelAPIView(viewsets.ModelViewSet):
    """
    GET - конкретный продукт по ID  или все продукты сразу у пользователя
    UPDATE + DELETE - конкретный продукт

    """

    permission_classes = [IsAuthenticated]
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

    def get_queryset(self):
        return ProductModel.objects.filter(user_account=self.request.user)


class QuestionsModelListAPIView(ListAPIView):
    """
    Получить список вопросов по id категории

    """

    model = QuestionsProductsModel
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionModelSerializer

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return QuestionsProductsModel.objects.filter(category__id=category_id).all()


class AnswerListAPIView(CreateAPIView):
    """
    Создать ответы на вопросы

    """

    permission_classes = [IsAuthenticated]
    serializer_class = AnswerCreateSerializer

    def get_serializer(self, *args, **kwargs):
        """if an array is passed, set serializer to many"""
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(AnswerListAPIView, self).get_serializer(*args, **kwargs)
