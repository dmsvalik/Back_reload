import os

from django.core.asgi import get_asgi_application


# это обязательно должно быть до остальных импортов
# в противном случае будет выброшено AppRegistryNotReady
django_asgi_app = get_asgi_application()


from app.chat.middleware import JWTAuthMiddlewareStack  # noqa
from app.chat.routing import websocket_urlpatterns  # noqa: E402

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa
from channels.security.websocket import AllowedHostsOriginValidator  # noqa


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
