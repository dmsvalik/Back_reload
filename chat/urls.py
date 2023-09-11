from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
# from chat.api import MessageModelViewSet, UserModelViewSet
from .views import index, room

router = DefaultRouter()
# router.register(r'message', MessageModelViewSet, basename='message-api')
# router.register(r'user', UserModelViewSet, basename='user-api')


urlpatterns = [
    # path(r'api/v1/', include(router.urls)),
    path("chat/", index, name="index"),
    path(r"chat/<str:room_name>/", room, name="room"),

    # path('', login_required(
    #     TemplateView.as_view(template_name='chat/chat.html')), name='home'),
]