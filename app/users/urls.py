from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views

from .views import CustomUserViewSet, CustomTokenObtainPairView

user_router = routers.DefaultRouter()
user_router.register(r"users", CustomUserViewSet, basename="custom_users")

urlpatterns = [
    path('auth/', include(user_router.urls), name="authentication", ),
    path("auth/jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("auth/jwt/refresh/", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    path("auth/jwt/verify/", views.TokenVerifyView.as_view(), name="jwt-verify"),
]
