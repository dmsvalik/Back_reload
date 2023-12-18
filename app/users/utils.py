from django.db.models import Sum

from app.orders.models import OrderFileData, OrderModel
from app.users.models import UserAccount

def calculate_order_file_sizes_with_cookie_key(
        user_obj: UserAccount,
        cookie_key: str) -> tuple[int] | None:
    """
    Суммирует размеры на яндекс диске и на сервере 1 заказа
    Взвращает кортеж где:
    1 элемент сумма всех файлов этого заказа на облачном хранилище
    2 элемент сумма всех файлов заказа на сервере
    """
    order = (
        OrderModel.objects
        .filter(key=cookie_key, user_account__isnull=True)
        .first()
        )

    if order:
        order.user_account = user_obj
        order.save()

        sizes = (
            OrderFileData.objects
            .filter(order_id__pk=order.pk)
            .aggregate(
            cloud_size=Sum("yandex_size"),
            server_size=Sum("server_size")
            )
        )
        return (sizes.get("cloud_size"), sizes.get("server_size"))
    return None
