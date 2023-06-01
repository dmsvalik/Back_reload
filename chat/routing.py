from chat import consumers
from django.urls import path



websocket_urlpatterns = [
    # url(r'^ws$', consumers.ChatConsumer),
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]