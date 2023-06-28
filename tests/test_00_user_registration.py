import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from rest_framework import status as st

from tests.fixtures.fixture_user import (
    url_users, test_user_data_1, user_invalid_data_1, user_invalid_data_2, test_user_data_2, test_user_data_3,
    url_activation, user_minimum_data
)


User = get_user_model()
pytestmark = pytest.mark.users


class Test00UserRegistration:
    """Тестирование регистрации пользователей."""

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize(
        "valid_data", [
            user_minimum_data,
            test_user_data_1,
            test_user_data_2,
            test_user_data_3,
        ]
    )
    def test_00_valid_data_user_signup(self, api_client, valid_data):
        """Тест регистрации пользователя с валидными данными."""
        outbox_before_count = len(mail.outbox)
        request_type = 'POST'
        response = api_client.post(url_users, data=valid_data)
        outbox_after = mail.outbox
        assert response.status_code != st.HTTP_404_NOT_FOUND, (
            f'Эндпойнт `{url_users}` не найден, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code != st.HTTP_400_BAD_REQUEST, (
            f'Проверьте, что при {request_type} запросе `{url_users}` с валидными данными '
            f'передаются все обязательные поля'
        )
        code = st.HTTP_201_CREATED
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{url_users}` с валидными данными '
            f'создаётся пользователь и возвращается статус {code}'
        )
        response_json = response.json()
        for field in valid_data:
            if field == 'password':
                continue
            assert field in response_json and valid_data.get(field) == response_json.get(field), (
                f'Проверьте, что при {request_type} запросе `{url_users}` с валидными данными '
                f'в ответ приходит созданный объект пользователя в виде словаря'
            )
        new_user = User.objects.filter(email=valid_data['email'])
        assert new_user.exists(), (
            f'Проверьте, что при {request_type} запросе `{url_users}` с валидными данными '
            f'в БД создается пользователь и возвращается статус {code}'
        )
        assert len(outbox_after) == outbox_before_count + 1, (
            f'Проверьте, что при {request_type} запросе `{url_users}` с валидными данными '
            f'пользователю отправляется email с кодом подтверждения'
        )
        new_user.delete()

    @pytest.mark.django_db
    def test_00_unauthorized_request(self, api_client):
        """Тест отсутствия доступа неавторизованным пользователям."""
        response = api_client.get(url_users)
        response_type = 'GET'
        assert response.status_code == st.HTTP_401_UNAUTHORIZED, (
            f'Проверьте, что при {response_type} запросе `{url_users}` неавторизованным пользователям '
            f'доступ запрещён'
        )

    # @pytest.mark.skip(reason='Разобраться с сериализаторами регистрации пользователей - обязательные поля!')
    @pytest.mark.django_db(transaction=True)
    def test_00_nodata_signup(self, api_client):
        """Тест попытки регистрации с пустыми полями."""
        request_type = 'POST'
        response = api_client.post(url_users)

        assert response.status_code != st.HTTP_404_NOT_FOUND, (
            f'Эндпойнт `{url_users}` не найден, проверьте этот адрес в *urls.py*'
        )
        code = st.HTTP_400_BAD_REQUEST
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{url_users}` без параметров '
            f'не создается пользователь и возвращается статус {code}'
        )
        response_json = response.json()
        empty_fields = ['email', 'name', 'password']
        for field in empty_fields:
            assert (field in response_json.keys()
                    and isinstance(response_json[field], list)), (
                f'Проверьте, что при {request_type} запросе `{url_users}` без параметров '
                f'в ответе есть сообщение о том, какие поля не заполнены'
            )

    @pytest.mark.now
    # @pytest.mark.skip(reason='Добавить валидацию всех полей')
    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize(
        "invalid_data", [
            user_invalid_data_1,
            user_invalid_data_2,
        ]
    )
    def test_00_invalid_data_signup(self, api_client, invalid_data):
        """Тест регистрации пользователей с невалидными данными."""
        request_type = 'POST'
        response = api_client.post(url_users, data=invalid_data)

        assert response.status_code == st.HTTP_400_BAD_REQUEST, (
            f'Проверьте, что при {request_type} запросе `{url_users}` с невалидными данными - '
            f'не создается пользователь и возвращается статус 400'
        )

        response_json = response.json()
        invalid_fields = ['email', 'name', 'password', 'person_telephone', 'surname']
        for field in invalid_fields:
            assert (field in response_json.keys()
                    and isinstance(response_json[field], list)
                    ), (
                # f'Проверьте, что при {request_type} запросе `{url_users}` с невалидными данными - '
                # f'в ответе есть сообщение о том, какие поля заполнены неправильно'
                f'{response_json.keys()}'
            )

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize(
        "valid_data", [
            test_user_data_1,
        ]
    )
    def test_00_same_email_user_signup(self, api_client, valid_data):
        """Тест повторной регистрации пользователя."""
        request_type = 'POST'
        api_client.post(url_users, data=valid_data)
        response = api_client.post(url_users, data=valid_data)
        code = st.HTTP_400_BAD_REQUEST
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{url_users}` нельзя создать '
            f'пользователя, email которого уже зарегистрирован, и возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_user_activation(self, api_client):
        """Тест активации пользователя."""

        """Регистрация пользователя."""
        api_client.post(url_users, data=test_user_data_1)

        """Получение кода подтверждения для активации."""
        mail_body = mail.outbox[-1].body
        regex = r'(?P<url>https?://[^\s]+)'
        link = re.search(regex, mail_body).group()
        data = link.split('/')
        activation_data = {
            'uid': data[-2],
            'token': data[-1]
        }

        """Активация пользователя."""
        response = api_client.post(url_activation, data=activation_data)
        code = st.HTTP_204_NO_CONTENT
        assert response.status_code == code, (
            f'Проверьте, что при POST запросе {url_activation} с валидными данными - возвращается статус {code}'
        )
