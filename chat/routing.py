from chat import consumers
from django.urls import re_path



websocket_urlpatterns = [
    # url(r'^ws$', consumers.ChatConsumer),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]