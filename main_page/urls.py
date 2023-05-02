from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from .views import PersonalClientAPIView

from . import views

urlpatterns = [
    path('api/v1/personal_data/', PersonalClientAPIView.as_view()),
]
