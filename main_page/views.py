from django.forms import model_to_dict
from djoser.views import UserViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import UserFedbackSerializer
from .models import UserFeedback
import requests


class FeedbackViewSet(viewsets.ModelViewSet):
    '''
    Сохранение обращения клиента на главной странице
    '''
    queryset = UserFeedback.objects.all()
    serializer_class = UserFedbackSerializer
    http_method_names = ['get', 'post', 'delete']


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        # this line is the only change from the base implementation.
        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}
        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response({'активация': 'активация аккаунта прошла успешно'})


