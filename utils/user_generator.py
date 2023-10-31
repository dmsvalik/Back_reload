import random
import string

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from main_page.models import UserAccount
from main_page.serializers import TokenObtainSerializer


@api_view(["GET"])
@permission_classes([AllowAny, ])
def user_generator(request):
    generated_email = ''.join(random.choices(
        string.ascii_lowercase,
        k=10
    )) + '@fakeuser.fake'
    while UserAccount.objects.filter(email=generated_email).exists():
        generated_email = ''.join(random.choices(
            string.ascii_lowercase,
            k=10
        )) + '@fakeuser.fake'
    generated_telephone = '+7' + ''.join(random.choices(
        string.digits,
        k=10
    ))
    while UserAccount.objects.filter(person_telephone=generated_telephone).exists():
        generated_telephone = '+7' + ''.join(random.choices(
            string.digits,
            k=10
        ))
    try:
        fake_user = UserAccount.objects.create(
            email=generated_email,
            name='FakeUser',
            person_telephone=generated_telephone,
            surname='FakeUser',
            password='generateduser1',
        )
        fake_user.set_password('generateduser1')
        fake_user.is_active = True
        fake_user.save()
    except Exception as er:
        print(er)
        # raise какой то ошибки
    serializer = TokenObtainSerializer(data={
        'email': generated_email,
        'password': 'generateduser1'

    })
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data)
