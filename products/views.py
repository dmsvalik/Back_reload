from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from rest_framework import viewsets

from .models import CardModel, CategoryModel, ProductModel, ProductImageModel
from .serializers import CardModelSerializer, CategoryModelSeializer, ProductModelSerializer, ProductImageSerializer


class CardModelAPIView(APIView):
    '''
    Получить список комнат - кухня, спалья и т.д.

    '''

    permission_classes = [AllowAny]
    def get(self, request):
        p = CardModel.objects.all()
        return Response({'personal_data': CardModelSerializer(p, many=True).data})


class CategoryModelListAPIView(ListAPIView):
    '''
    Получить список категорий по id карточки

    '''
    model = CategoryModel
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSeializer

    def get_queryset(self):
        card_id = self.kwargs['card_id']
        return CategoryModel.objects.filter(card__id=card_id).all()


class ProductModelCreateAPIView(CreateAPIView):
    '''
    Создать продукт заказа

    '''
    permission_classes = [IsAuthenticated]
    serializer_class = ProductModelSerializer


class ProductModelAPIView(viewsets.ModelViewSet):
    '''
    GET - конкретный продукт по ID  или все продукты сразу у пользователя
    UPDATE + DELETE - конкретный продукт

    '''
    permission_classes = [IsAuthenticated]
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

    def get_queryset(self):
        return ProductModel.objects.filter(user_account=self.request.user)


class ProductImageViewSet(ListAPIView):
    '''Проверка картинок по продукту + создание картинок с привязкой к продукту'''

    queryset = ProductImageModel.objects.all()
    serializer_class = ProductImageSerializer

    #достаем все объекты пользователя
    def get_queryset(self):
        user = self.request.user
        return ProductImageModel.objects.filter(product_id__user_account=user)

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        product_id = request.data['product_id']
        get_instance = ProductModel.objects.get(id=product_id)
        image = ProductImageModel.objects.create(image=file, product_id=get_instance)
        return Response({'Загрузка фото': 'Успешно прошла'})