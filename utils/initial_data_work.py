from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from main_page.models import UserQuota, UserAccount
from products.models import CardModel


class InitialData(object):

    name = 'user'
    surname = 'user_surname_'
    person_telephone = '+7900123456'
    domain = '@mail.ru'
    password = 'User007!'

    def create_initial_admin(self):
        try:
            admin = UserAccount.objects.create_superuser(
                email=f'admin{self.domain}',
                name='admin',
                person_telephone=f'+79113332244',
                surname='admin_surname',
                password='admin',
            )
            admin_data = {'email': f'admin{self.domain}', 'password': 'admin'}
            return Response({'success': admin_data})
        except Exception as e:
            return Response({'error': str(e)})

    def create_initial_users(self):
        names = ['Алексей', 'Александр', 'Мария', 'Оксана', 'Егор']
        surname = ['Иванов', 'Смирнов', 'Кузнецова', 'Михайлова', 'Пронин']

        try:
            for x in range(len(names)):
                user = UserAccount.objects.get_or_create(
                    email=f'user{x}{self.domain}',
                    name=names[x],
                    person_telephone=f'{self.person_telephone}{x}',
                    surname=surname[x],
                    password=self.password,
                )
                print(user)
                user[0].is_active = True
                user[0].save()
            return Response({'success': f'users created'})
        except Exception as e:
            print(e)
            return Response({'error': str(e)})

    def create_initial_categories(self):
        categories = ['kitchen', 'table']
        try:
            for x in range(len(categories)):
                CardModel.objects.get_or_create(
                    name=categories[x],
                )
            return Response({'success': f'categories created'})
        except Exception as e:
            print(e)
            return Response({'error': str(e)})


initial_db = InitialData()


@api_view(["POST"])
@permission_classes([AllowAny])
def create_admin(request):
    result = initial_db.create_initial_admin()
    print(result)
    return result


@api_view(["POST"])
@permission_classes([AllowAny])
def create_users(request):
    result = initial_db.create_initial_users()
    print(result)
    return result


@api_view(["POST"])
@permission_classes([AllowAny])
def create_categories(request):
    result = initial_db.create_initial_categories()
    print(result)
    return result

