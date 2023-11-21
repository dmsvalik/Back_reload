from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views

from .views import ActivateUser, reset_password, CustomUserViewSet, CustomTokenObtainPairView

router = routers.SimpleRouter()
user_router = routers.DefaultRouter()
user_router.register(r"users", CustomUserViewSet, basename="custom_users")

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
    path('auth2/', include(user_router.urls), name="auth2"),
    path("auth2/jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("auth2/jwt/refresh/", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    path("auth2/jwt/verify/", views.TokenVerifyView.as_view(), name="jwt-verify"),
]
