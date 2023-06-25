import pytest
from django.contrib.auth import get_user_model
from django.core import mail

from main_page.email import EMAILS
from tests.common import auth_client
from tests.fixtures.fixture_user import url_signup, url_profile, user_full_data_1

User = get_user_model()

pytestmark = pytest.mark.users


class Test01UserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_profile_get(self, api_client):
        # auth_user = auth_client(user)
        # test_user = User.objects.filter(email=user_full_data_1['email'])
        api_client.post(url_signup, data=user_full_data_1)
        activation_data = EMAILS[user_full_data_1["email"]]
        response = api_client.post('http://127.0.0.1:8000/auth/users/activation/', data=activation_data)
        assert 1 == 2, (
            f'{response}'
        )

        # response = auth_user.get(url_profile)
        # assert response.status_code != 404, (
        #     f'Эндпойнт `{url_profile}` не найден, проверьте этот адрес в *urls.py*'
        # )
        # code = 200
        # assert response.status_code == code, (
        #     f'Проверьте, что при GET запросе `{url_profile}` авторизованным пользователем - возвращается статус {code}'
        # )

    @pytest.mark.django_db(transaction=True)
    def test_000_auth_superuser(self, user_superuser):
        auth_user = auth_client(user_superuser)
        response = auth_user.get(url_signup)
        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при GET запросе `{url_signup}` авторизованным пользователем - возвращается статус {code}'
        )

    # obj = mail.outbox[-1].body
    # regex_2 = "(?P<url>https?://[^\s]+)"
    # link = re.search(regex_2, obj).group()
    # url = link.split('/')
    # url_path = f'{url[-3]}/{url[-2]}/{url[-1]}/'
    # # assert 1 == 2, f'{url_path}'
    # response = api_client.get(url_path)
    # code = 200
    # assert response.status_code == code, (
    #     f'Проверьте, что при GET запросе `{url_path}` авторизованным пользователем - возвращается статус {code}'
    #     f'{response.json().keys()}'
    # )
