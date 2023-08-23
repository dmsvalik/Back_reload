from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from .yasg import urlpatterns as doc_urls
from main_page.serializers import CutomObtainPairView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main_page.urls")),
    path("", include("products.urls")),
    path("", include("orders.urls")),
    path('auth/jwt/create/', CutomObtainPairView.as_view(), name='customtoken'),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path('admin/', admin.site.urls),
    path('', include('main_page.urls')),
    path('', include('products.urls')),
    path('', include('orders.urls')),
    path('', include('chat.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'},
         name='logout')
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
