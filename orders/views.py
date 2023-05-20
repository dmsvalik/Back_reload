from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from rest_framework import viewsets
from .models import *
from .serializers import *



class OrderImageViewSet(ListAPIView):
    '''Проверка картинок по продукту + создание картинок с привязкой к продукту'''

    queryset = OrderImageModel.objects.all()
    serializer_class = OrderImageSerializer

    # достаем все объекты пользователя
    def get_queryset(self):
        user = self.request.user
        return OrderImageModel.objects.filter(order_id__user_account=user)

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        order_id = request.data['order_id']
        get_instance = OrderModel.objects.get(id=order_id)
        image = OrderImageModel.objects.create(image=file, order_id=get_instance)
        return Response({'Загрузка фото': 'Успешно прошла'})

