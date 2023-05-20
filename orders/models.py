from django.db import models
from main_page.models import UserAccount
from products.models import CardModel


STATE_CHOICES = (
    ('auction', 'Аукцион'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)


class OrderModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    card_id = models.ForeignKey(CardModel, on_delete=models.CASCADE, null=False,  blank=True)
    order_time = models.DateTimeField('Дата создания заказа', auto_now=True)
    order_description = models.CharField('Описание заказа', max_length=300, blank=True)
    state = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=15)

    class Meta:
        verbose_name = 'Заказ состоящий из продуктов'
        verbose_name_plural = 'Заказ состоящий из продуктов'




# создаем путь - папка image далее папка(id пользователя), далее папка(id продукта)
def nameFile(instance, filename):
    return '/'.join(['images', str(instance.order_id.user_account.id), str(instance.order_id.id), filename])


class OrderImageModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    order_id = models.ForeignKey(OrderModel, related_name='order_id', on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)

    class Meta:
        verbose_name = 'Изображения - заказ пользователя'
        verbose_name_plural = 'Изображения - заказ пользователя'

    def __str__(self):
        return str(self.id)


