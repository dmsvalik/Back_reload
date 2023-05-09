from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny

from .models import CardModel, CategoryModel
from .serializers import CardModelSerializer, CategoryModelSeializer


class CardModelAPIView(APIView):
    '''
    Получить список комнат - кухня, спалья и т.д.

    '''

    permission_classes = [AllowAny]
    def get(self, request):
        p = CardModel.objects.all()
        print('1')
        print('---------------')
        return Response({'personal_data': CardModelSerializer(p, many=True).data})


class CategoryModelListAPIView(ListAPIView):
    '''
        Получить список категорий по id карточки

    '''
    model = CategoryModel
    permission_classes = [AllowAny]
    serializer_class = CategoryModelSeializer

    def get_queryset(self):
        card_id = self.kwargs['card_id']
        return CategoryModel.objects.filter(card__id=card_id).all()