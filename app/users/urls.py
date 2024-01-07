from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views

from .swagger_documentation.users import TokenJWTVerify, TokenJWTRefresh
from .views import CustomUserViewSet, CustomTokenObtainPairView

from drf_yasg.utils import swagger_auto_schema


user_router = routers.DefaultRouter()
user_router.register(r"users", CustomUserViewSet, basename="custom_users")


def is_route_selected(url_pattern):
    urls = ["users/reset_email/", "users/reset_email_confirm/", "users/{id}/"]

    for u in urls:
        match = url_pattern.resolve(u)
        if match:
            return False
    return True


selected_user_routes = list(filter(is_route_selected, user_router.urls))

# Декораторы документации SWAGGER
decorated_jwt_verify_view = swagger_auto_schema(**TokenJWTVerify.__dict__)(
    views.TokenVerifyView.as_view()
)

decorated_jwt_refresh_view = swagger_auto_schema(**TokenJWTRefresh.__dict__)(
    views.TokenRefreshView.as_view()
)

urlpatterns = [
    path(
        "auth/",
        include(selected_user_routes),
        name="authentication",
    ),
    path(
        "auth/jwt/create/",
        CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path(
        "auth/jwt/refresh/",
        decorated_jwt_refresh_view,
        name="jwt-refresh",
    ),
    path("auth/jwt/verify/", decorated_jwt_verify_view, name="jwt-verify"),
]
