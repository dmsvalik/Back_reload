# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.core.asgi import get_asgi_application

# from chat import routing as core_routing, consumers

# import os
# from django.urls import path

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# django_asgi_app = get_asgi_application()

# # application = ProtocolTypeRouter({
# #     "websocket": AuthMiddlewareStack(
# #         URLRouter(
# #             core_routing.websocket_urlpatterns
# #         )
# #     ),
# # })

# from chat.consumers import ChatConsumer

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter([path('ws/<str:room_name>/', ChatConsumer.as_asgi())]))
#         ),
#     }
# )
