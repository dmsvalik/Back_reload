from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserFedbackSerializer
from .models import UserFeedback


class FeedbackViewSet(viewsets.ModelViewSet):
    '''
    Сохранение обращения клиента на главной странице
    '''
    queryset = UserFeedback.objects.all()
    serializer_class = UserFedbackSerializer
    http_method_names = ['get', 'post', 'delete']

