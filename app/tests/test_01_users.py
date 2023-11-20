import pytest
from django.contrib.auth import get_user_model
from rest_framework import status as st

from app.tests.fixtures.fixture_user import url_profile, url_users, test_user_data, test_user_new_data


User = get_user_model()
pytestmark = pytest.mark.users


class Test01UserAPI:

    @pytest.mark.now
    @pytest.mark.django_db(transaction=True)
    def test_01_profile_get(self, user_client):
        """Тест получения данных из профиля пользователя."""
        response = user_client.get(url_profile)
        assert response.status_code != st.HTTP_404_NOT_FOUND, (
            f'Эндпойнт `{url_profile}` не найден'
        )
        assert response.status_code == st.HTTP_200_OK, (
            f'Проверьте, что при GET запросе `{url_profile}` авторизованным пользователем - возвращается статус 200'
        )
        response_json = response.json()
        for field in test_user_data:
            if field == 'password':
                continue
            assert field in response_json and test_user_data.get(field) == response_json.get(field), (
                f'Проверьте, что при GET запросе `{url_profile}` авторизованным пользователем '
                f'в ответ приходит созданный объект пользователя в виде словаря, со всеми полями'
            )

    @pytest.mark.django_db(transaction=True)
    def test_02_profile_patch(self, user_client):
        """Тест редактирования профиля пользователя."""
        for field, value in test_user_new_data.items():
            if field in ('email', 'password'):
                continue
            user_client.patch(url_profile, data={field: value})

        response = user_client.get(url_profile)
        response_json = response.json()
        for field in test_user_new_data:
            if field in ('email', 'password'):
                continue
            assert field in response_json and test_user_new_data.get(field) == response_json.get(field)

    @pytest.mark.skip(reason='Определиться с удалением пользователей')
    @pytest.mark.django_db(transaction=True)
    def test_03_profile_delete(self, user):
        """Тест удаления профиля пользователя."""
        pass

    @pytest.mark.django_db(transaction=True)
    def test_04_user_by_id_get(self, user, admin_client):
        """Тест получения данных пользователя по его `id`."""
        response = admin_client.get(f'{url_users}{user.id}/')
        assert response.status_code != st.HTTP_404_NOT_FOUND, (
            f'Эндпойнт `{url_users}{user.id}/` не найден'
        )
        assert response.status_code == st.HTTP_200_OK, (
            f'Проверьте, что при GET запросе `{url_users}{user.id}/` админом - возвращается статус 200'
        )
        response_json = response.json()
        for field in test_user_data:
            if field == 'password':
                continue
            assert field in response_json and test_user_data.get(field) == response_json.get(field), (
                f'Проверьте, что при GET запросе `{url_users}{user.id}/` админом '
                f'в ответ приходит данные пользователя, со всеми полями'
            )

    @pytest.mark.django_db(transaction=True)
    def test_05_user_by_id_patch(self, user_1, admin_client):
        """Тест редактирования данных пользователя по его `id`."""
        for field, value in test_user_new_data.items():
            if field in ('email', 'password'):
                continue
            admin_client.patch(f'{url_users}{user_1.id}/', data={field: value})

        response = admin_client.get(f'{url_users}{user_1.id}/')
        response_json = response.json()
        for field in test_user_new_data:
            if field in ('email', 'password'):
                continue
            assert field in response_json and test_user_new_data.get(field) == response_json.get(field)

    @pytest.mark.skip(reason='Определиться с удалением пользователей')
    @pytest.mark.django_db(transaction=True)
    def test_06_user_by_id_delete(self, admin_client):
        """Тест удаления пользователя по его `id`."""
        pass
