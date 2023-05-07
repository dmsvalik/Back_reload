from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny

from .models import CardModel
from .serializers import CardModelSerializer


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
