from app.main_page.serializers import CutomObtainPairView

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.main_page.urls")),
    path("", include("app.products.urls")),
    path("", include("app.orders.urls")),
    path("", include("app.utils.urls")),
    path("", include("app.chat.urls")),
    path("", include("app.users.urls")),
    path("", include("app.questionnaire.urls")),
    path('auth/jwt/create/', CutomObtainPairView.as_view(), name='customtoken'),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
