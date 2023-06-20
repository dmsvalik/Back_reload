import pytest
from django.contrib.auth import get_user_model
from django.core import mail


User = get_user_model()

pytestmark = pytest.mark.users


class TestUserRegistration:
    # url_signup = '/auth/users/'
    # url_token = '/auth/jwt/create/'
    url_create_user = '/auth/users/'

    @pytest.mark.django_db(transaction=True)
    def test_valid_data_create_user(self, client):
        """Тест создания пользователя с валидными данными."""
        outbox_before_count = len(mail.outbox)
        valid_data = {
            'email': 'testuser@project.fake',
            'name': 'TestUser',
            'password': '12345678',
            'person_telephone': '9000000000',
            'surname': 'TestUser',
        }
        request_type = 'POST'
        response = client.post(self.url_create_user, data=valid_data)
        outbox_after = mail.outbox
        assert response.status_code != 404, (
            f'Страница `{self.url_create_user}` не найдена, проверьте этот адрес в *urls.py*'
        )
        code = 201
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_create_user}` с валидными данными '
            f'от имени администратора, создается пользователь и возвращается статус {code}'
        )
        response_json = response.json()
        for field in valid_data:
            if field == 'password':
                continue
            assert field in response_json and valid_data.get(field) == response_json.get(field), (
                f'Проверьте, что при {request_type} запросе `{self.url_create_user}` с валидными данными '
                f'от имени администратора, в ответ приходит созданный объект пользователя в виде словаря'
            )
        new_user = User.objects.filter(email=valid_data['email'])
        assert new_user.exists(), (
            f'Проверьте, что при {request_type} запросе `{self.url_create_user}` с валидными данными '
            f'от имени администратора, в БД создается пользователь и возвращается статус {code}'
        )
        assert len(outbox_after) == outbox_before_count + 1, (
            f'Проверьте, что при {request_type} запросе `{self.url_create_user}` с валидными данными '
            f'от имени администратора, пользователю отправляется email с кодом подтверждения'
        )
        new_user.delete()
