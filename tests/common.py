from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def auth_client(user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'JWT {refresh.access_token}')
    return client
