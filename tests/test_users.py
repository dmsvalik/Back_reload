import pytest
from django.contrib.auth import get_user_model
from django.core import mail

from tests.fixtures.fixture_user import (
    user_full_data_1, user_invalid_data_1, user_invalid_data_2, user_full_data_2, user_full_data_3, url_signup
)

User = get_user_model()

pytestmark = pytest.mark.users


class TestUserRegistration:
    """Тестирование регистрации пользователей."""

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize(
        "valid_data", [
            # user_minimum_data,
            user_full_data_1,
            user_full_data_2,
            user_full_data_3,
        ]
    )
    def test_valid_data_user_signup(self, api_client, valid_data):
        """Тест регистрации пользователя с валидными данными."""
        outbox_before_count = len(mail.outbox)
        request_type = 'POST'
        response = api_client.post(url_signup, data=valid_data)
        outbox_after = mail.outbox
        assert response.status_code != 404, (
            f'Эндпойнт `{url_signup}` не найден, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code != 400, (
            f'Проверьте, что при {request_type} запросе `{url_signup}` с валидными данными '
            f'передаются все обязательные поля'
        )
        code = 201
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{url_signup}` с валидными данными '
            f'создаётся пользователь и возвращается статус {code}'
        )
        response_json = response.json()
        for field in valid_data:
            if field == 'password':
                continue
            assert field in response_json and valid_data.get(field) == response_json.get(field), (
                f'Проверьте, что при {request_type} запросе `{url_signup}` с валидными данными '
                f'в ответ приходит созданный объект пользователя в виде словаря'
            )
        new_user = User.objects.filter(email=valid_data['email'])
        assert new_user.exists(), (
            f'Проверьте, что при {request_type} запросе `{url_signup}` с валидными данными '
            f'в БД создается пользователь и возвращается статус {code}'
        )
        assert len(outbox_after) == outbox_before_count + 1, (
            f'Проверьте, что при {request_type} запросе `{url_signup}` с валидными данными '
            f'пользователю отправляется email с кодом подтверждения'
        )
        new_user.delete()

    @pytest.mark.django_db
    def test_unauthorized_request(self, api_client):
        """Тест отсутствия доступа неавторизованным пользователям."""
        response = api_client.get(url_signup)
        response_type = 'GET'
        assert response.status_code == 401, (
            f'Проверьте, что при {response_type} запросе `{url_signup}` неавторизованным пользователям '
            f'доступ запрещён'
        )

    @pytest.mark.skip(reason='Разобраться с сериализаторами регистрации пользователей - обязательные поля!')
    @pytest.mark.django_db(transaction=True)
    def test_nodata_signup(self, client):
        """Тест попытки регистрации с пустыми полями."""
        request_type = 'POST'
        response = client.post(url_signup)

        assert response.status_code != 404, (
            f'Эндпойнт `{url_signup}` не найден, проверьте этот адрес в *urls.py*'
        )
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{url_signup}` без параметров '
            f'не создается пользователь и возвращается статус {code}'
        )
        response_json = response.json()
        empty_fields = ['email', 'name', 'password', 'person_telephone', 'surname']
        for field in empty_fields:
            assert (field in response_json.keys()
                    and isinstance(response_json[field], list)), (
                f'Проверьте, что при {request_type} запросе `{url_signup}` без параметров '
                f'в ответе есть сообщение о том, какие поля не заполнены'
            )

    @pytest.mark.skip(reason='Добавить валидацию всех полей')
    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize(
        "invalid_data", [
            user_invalid_data_1,
            user_invalid_data_2,
        ]
    )
    def test_invalid_data_signup(self, client, invalid_data):
        """Тест регистрации пользователей с невалидными данными."""
        request_type = 'POST'
        response = client.post(url_signup, data=invalid_data)

        code = 400
        assert response.status_code == 400, (
            f'Проверьте, что при {request_type} запросе `{url_signup}` с невалидными данными - '
            f'не создается пользователь и возвращается статус {code}'
        )

        response_json = response.json()
        invalid_fields = ['email', 'name', 'password', 'person_telephone', 'surname']
        for field in invalid_fields:
            assert (field in response_json.keys()
                    and isinstance(response_json[field], list)), (
                f'Проверьте, что при {request_type} запросе `{url_signup}` с невалидными данными - '
                f'в ответе есть сообщение о том, какие поля заполнены неправильно'
            )

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize(
        "valid_data", [
            user_full_data_1,
        ]
    )
    def test_same_email_user_signup(self, client, valid_data):
        """Тест повторной регистрации пользователя."""
        request_type = 'POST'
        client.post(url_signup, data=valid_data)
        response = client.post(url_signup, data=valid_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{url_signup}` нельзя создать '
            f'пользователя, email которого уже зарегистрирован, и возвращается статус {code}'
        )
