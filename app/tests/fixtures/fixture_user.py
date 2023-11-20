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

valid_name = 'user'
valid_surname = 'Стив'
valid_email = 'user@mail.ru'
valid_password = 'userPassword!1'
valid_telephone = '+7911000230'

test_admin = {
    'email': 'testadmin@project.fake',
    'name': 'TestAdmin',
    'password': 'L1Z,D2xo=x]!XbqQ',
    'person_telephone': '+79000000000',
    'surname': 'TestAdminoff',
}

# валидные пользователи для тестов
test_user_data = {
    'email': valid_email,
    'name': valid_name,
    'password': valid_password,
    'person_telephone': valid_telephone + '0',
    'surname': valid_surname,
}
test_user_data_1 = {
    'email': '1' + valid_email,
    'name': 'a' + valid_name,
    'password': valid_password,
    'person_telephone': valid_telephone + '1',
    'surname': 'a' + valid_surname,
}
test_user_data_2 = {
    'email': '2' + valid_email,
    'name': 'b' + valid_name,
    'password': valid_password,
    'person_telephone': valid_telephone + '2',
    'surname': 'b' + valid_surname,
}
test_user_data_3 = {
    'email': '3' + valid_email,
    'name': 'c' + valid_name,
    'password': valid_password,
    'person_telephone': valid_telephone + '3',
    'surname': 'c' + valid_surname,
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

# невалидные пользователи для тестов
user_invalid_data_email_1 = {
    'email': 'invalid_email',
    'name': valid_name,
    'password': valid_password,
    'person_telephone': valid_telephone,
    'surname': valid_surname,
}
user_invalid_password_2 = {
    'email': valid_email,
    'name': valid_name,
    'password': '!@#',
    'person_telephone': valid_telephone,
    'surname': valid_surname,
}
user_invalid_name_3 = {
    'email': valid_email,
    'name': valid_name,
    'password': '!@#',
    'person_telephone': valid_telephone,
    'surname': valid_surname,
}
user_invalid_telephone_4 = {
    'email': valid_email,
    'name': valid_name,
    'password': valid_password,
    'person_telephone': '+783433',
    'surname': valid_surname,
}
