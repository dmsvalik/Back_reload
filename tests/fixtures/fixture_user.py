import pytest
from rest_framework.test import APIClient

from tests.common import auth_client


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_client(user):
    return auth_client(user)


@pytest.fixture
def admin_client(user_admin):
    return auth_client(user_admin)


@pytest.fixture
def user_superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        email='testsuperuser@project.fake',
        name='TestSuperuser',
        password='32[fN_r7/z5v`o&N',
        person_telephone='+79000000000',
        surname='TestSuperuser',
    )


@pytest.fixture
def user_admin(django_user_model):
    user = django_user_model.objects.create(**test_admin)
    user.is_active = True
    user.is_admin = True
    user.is_staff = True
    user.save()
    return user


@pytest.fixture
def user(django_user_model):
    user = django_user_model.objects.create(**test_user_data)
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def user_1(django_user_model):
    user = django_user_model.objects.create(**test_user_data_1)
    user.is_active = True
    user.save()
    return user


url_users = '/auth/users/'
url_activation = '/auth/users/activation/'
url_token = '/auth/jwt/create/'
url_profile = '/auth/users/me/'
test_admin = {
    'email': 'testadmin@project.fake',
    'name': 'TestAdmin',
    'password': 'L1Z,D2xo=x]!XbqQ',
    'person_telephone': '+79000000000',
    'surname': 'TestAdminoff',
}
test_user_data = {
    'email': 'testuser@project.fake',
    'name': 'TestUser',
    'password': 'L1Z,D2xo=x]!XbqQ',
    'person_telephone': '+79000000000',
    'surname': 'TestUseroff',
}
test_user_data_1 = {
    'email': 'test_user_1@project.fake',
    'name': 'Первый',
    'password': '_>Ke:[Bs<kSo[H9T',
    'person_telephone': '+79000000000',
    'surname': 'Пользователь',
}
test_user_data_2 = {
    'email': 'fulluser2@mail.fake',
    'name': 'Второй',
    'password': 'C1Pt}&Rq*4^!A*)A',
    'person_telephone': '+79000000000',
    'surname': 'Пользователь',
}
test_user_data_3 = {
    'email': 'fulluser3@mail.fake',
    'name': 'TestUser',
    'password': '>-Kc-k]_1UwVy1>^',
    'person_telephone': '+79000000000',
    'surname': 'TestUseroff',
}
test_user_new_data = {
    'email': 'new_test_user@project.fake',
    'name': 'UpdatedName',
    'password': 'K)x2MkG{z>fn.QEC',
    'person_telephone': '+79000000001',
    'surname': 'UpdatedSurname',
}
user_minimum_data = {
    'email': 'minuser@mail.fake',
    'name': 'MinUserName',
    'password': 's.GD4bBXo#;JS#Dt',
}
user_invalid_data_1 = {
    'email': 'invalid_email',
    'name': '123',
    'password': '1234578',
    'person_telephone': '8900',
    'surname': '321',
}
user_invalid_data_2 = {
    'email': 'invalid@email',
    'name': '@!=+-',
    'password': '!@#',
    'person_telephone': '0000000000',
    'surname': '-+=!@',
}
