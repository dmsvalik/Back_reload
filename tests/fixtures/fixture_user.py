import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        email='testsuperuser@project.fake',
        name='TestSuperuser',
        password='32[fN_r7/z5v`o&N',
        person_telephone='+79000000000',
        surname='TestSuperuser',
    )


url_signup = '/auth/users/'
url_token = '/auth/jwt/create/'
user_full_data_1 = {
    'email': 'fulluser@mail.fake',
    'name': 'TestUser',
    'password': '_>Ke:[Bs<kSo[H9T',
    'person_telephone': '+79000000000',
    'surname': 'TestUseroff',
}
user_full_data_2 = {
    'email': 'fulluser2@mail.fake',
    'name': 'TestUser',
    'password': 'C1Pt}&Rq*4^!A*)A',
    'person_telephone': '89000000000',
    'surname': 'TestUseroff',
}
user_full_data_3 = {
    'email': 'fulluser3@mail.fake',
    'name': 'TestUser',
    'password': '>-Kc-k]_1UwVy1>^',
    'person_telephone': '9000000000',
    'surname': 'TestUseroff',
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
