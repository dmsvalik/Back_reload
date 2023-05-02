from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from .views import PersonalClientAPIView

from . import views

urlpatterns = [
    path('api/personal_client_data/', PersonalClientAPIView.as_view()),
    path('api/personal_client_data/<int:pk>', PersonalClientAPIView.as_view()),
]
