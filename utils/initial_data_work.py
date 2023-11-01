from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import datetime, timedelta, timezone

from main_page.models import UserQuota, UserAccount, ContractorData
from orders.models import OrderModel, STATE_CHOICES, OrderOffer
from products.models import CardModel


class InitialData(object):
    person_telephone_client = '+7900123456'
    person_telephone_contractor = '+7900123453'
    description = 'Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots ' \
                  'in a piece of classical Latin literature from 45 BC, making it over 2000 years old. '
    domain = '@mail.ru'
    password = 'User007!'

    def create_initial_admin(self):
        try:
            UserAccount.objects.create_superuser(
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

    def create_initial_categories(self):
        categories = ['kitchen', 'table']
        try:
            for x in range(len(categories)):
                CardModel.objects.get_or_create(
                    name=categories[x],)
            return Response({'success': f'categories created'})
        except Exception as e:
            return Response({'error': str(e)})

    def create_initial_contractors(self):
        names = ['Дмитрий', 'Анна', 'Олег']
        surname = ['Карпачин', 'Верескина', 'Донской']
        company_name = ['Икеа', 'Мебельный Центр', 'Кухни Мария']

        for x in range(len(names)):
            try:
                user = UserAccount.objects.create(
                    email=f'contractor{x}{self.domain}',
                    name=names[x],
                    person_telephone=f'{self.person_telephone_contractor}{x}',
                    surname=surname[x],
                    password=self.password,
                )
                user.is_active = True
                user.role = "contractor"
                user.save()

                ContractorData.objects.create(
                    user=user,
                    is_active=True,
                    company_name=company_name[x],
                    phone_number=f'{self.person_telephone_contractor}{x}',
                )
            except:
                pass
        return Response({'success': f'contractors created'})

    def create_initial_users(self):
        self.create_initial_categories()
        self.create_initial_contractors()
        self.create_initial_admin()

        names = ['Алексей', 'Александр', 'Мария', 'Оксана', 'Егор']
        surname = ['Иванов', 'Смирнов', 'Кузнецова', 'Михайлова', 'Пронин']

        for x in range(len(names)):
            try:
                user = UserAccount.objects.create(
                    email=f'user{x}{self.domain}',
                    name=names[x],
                    person_telephone=f'{self.person_telephone_client}{x}',
                    surname=surname[x],
                    password=self.password,
                )
                user.is_active = True
                user.save()
            except:
                pass

        all_clients = UserAccount.objects.filter(role='client', is_staff=False)
        all_contractors = ContractorData.objects.filter(is_active=True)

        for client in all_clients:
            total_orders = len(OrderModel.objects.filter(user_account=client))
            try:
                last_id = OrderModel.objects.last().id
            except:
                last_id = 1
            if total_orders < 8:

                for x in range(len(STATE_CHOICES)):
                    new_order = OrderModel.objects.create(
                        user_account=client,
                        order_time=datetime.now(tz=timezone.utc),
                        name=f'order_N_{last_id+x}_{client.email}',
                        order_description=self.description,
                        card_category=CardModel.objects.get(name='kitchen'),
                        state=STATE_CHOICES[x][0]
                    )

                # create 1 order expired status - offer -> can see offers
                expired_order = OrderModel.objects.create(
                    user_account=client,
                    order_time=datetime.now(tz=timezone.utc) + timedelta(days=1),
                    name=f'order_OFFER_EXPIRED_{client.email}',
                    order_description=f'',
                    card_category=CardModel.objects.get(name='kitchen'),
                    state='offer'
                )

                # create some offers
                total_orders_in_offer = OrderModel.objects.filter(user_account=client, state='offer')
                for order in total_orders_in_offer:
                    for x in range(len(all_contractors)):
                        OrderOffer.objects.create(
                            user_account=all_contractors[x].user,
                            order_id=order,
                            offer_price=f'24560{x}',
                            offer_execution_time=f'Выполним за: {x} мес.',
                            offer_description=f'Добрый день, мы представляем компанию - {all_contractors[x].company_name}'
                                              f' Нам необходимо уточнить некоторые моменты, напишите мне в чате',
                        )
        return Response({'success': f'users created'})


initial_db = InitialData()


@api_view(["POST"])
@permission_classes([AllowAny])
def create_admin(request):
    """ Create initial admin - admin@admin.ru / admin """
    result = initial_db.create_initial_admin()
    return result


@api_view(["POST"])
@permission_classes([AllowAny])
def create_users(request):
    """ Create initial 4 users with company-users + orders + offers """
    result = initial_db.create_initial_users()
    return result
