import pytest


@pytest.fixture
def user_superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        email='testsuperuser@project.fake',
        name='TestSuperuser',
        password='12345678',
        person_telephone='9000000000',
        surrname='TestSuperuser',
    )
