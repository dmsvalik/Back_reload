import traceback

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import decode as jwt_decode
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError


User = get_user_model()


async def map_headers(bheaders):
    headers = dict()
    for header, value in bheaders.items():
        new_header = header.decode("utf8")
        new_value = value.decode("utf8")
        headers[new_header] = new_value
    return headers


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            headers = await map_headers(dict(scope["headers"]))
            # это костыль для JavaScript, который не умеет в заголовки
            if headers.get("sec-websocket-protocol"):
                jwt_token = headers.get("sec-websocket-protocol")
                jwt_payload = self.get_payload(jwt_token)
                user_credentials = self.get_user_credentials(jwt_payload)
                user = await self.get_logged_in_user(user_credentials)
                scope["user"] = user
            else:
                scope["user"] = AnonymousUser()
        except (
            InvalidSignatureError,
            KeyError,
            ExpiredSignatureError,
            DecodeError,
        ):
            traceback.print_exc()
            scope["user"] = AnonymousUser()
        except Exception:
            scope["user"] = AnonymousUser()
        return await self.app(scope, receive, send)

    def get_payload(self, jwt_token):
        return jwt_decode(
            jwt_token,
            settings.SECRET_KEY,
            algorithms=settings.SIMPLE_JWT.get("ALGORITHM"),
        )

    def get_user_credentials(self, payload):
        """
        method to get user credentials from jwt token payload.
        defaults to user id.
        """
        return payload["user_id"]

    async def get_logged_in_user(self, user_id):
        return await self.get_user(user_id)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def JWTAuthMiddlewareStack(app):
    return JWTAuthMiddleware(AuthMiddlewareStack(app))
