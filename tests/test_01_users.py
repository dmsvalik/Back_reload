import pytest
from django.contrib.auth import get_user_model

from tests.common import auth_client
from tests.fixtures.fixture_user import url_signup

User = get_user_model()

pytestmark = pytest.mark.users


class Test01UserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_auth_superuser(self, user_superuser):
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
