from django.urls import path
from rest_framework import routers

from .views import ActivateUser, reset_password


router = routers.SimpleRouter()

urlpatterns = [
    path(
        "activate/<uid>/<token>",
        ActivateUser.as_view({"get": "activation"}),
        name="activation",
    ),
    path(
        "password/reset/confirm/<str:uid>/<str:token>",
        reset_password,
        name="reset_password",
    ),
]
