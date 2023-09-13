from functools import wraps
from django.http import HttpResponse
from .models import UserQuota
from orders.models import OrderOffer


def check_user_quota(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        user_id = request.user.id
        try:
            user_quota = UserQuota.objects.get(user_id=user_id)
        except UserQuota.DoesNotExist:
            return HttpResponse("Пользователь с указанным ID не найден", status=404)
        if user_quota.quota_cloud_size >= 3 * 1024 * 1024:
            return HttpResponse("Превышена квота в облаке (3 МБ). Удалите лишние файлы", status=400)
        if user_quota.total_server_size >= 5 * 1024 * 1024:
            return HttpResponse("Превышена квота на сервере (5 МБ). Удалите лишние файлы", status=400)
        if user_quota.total_traffic < 0:
            return HttpResponse("Превышен допустимый трафик. Дождитесь следующего месяца или обратитесь к администраторам", status=404)
        return func(request, *args, **kwargs)
    return wrapped


def check_file_type(allowed_types):
    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                file_extension = uploaded_file.name.split('.')[-1].lower()
                if file_extension not in allowed_types:
                    return HttpResponse("Недопустимый тип файла", status=400)
            return func(request, *args, **kwargs)
        return wrapped
    return decorator


def check_order_limit(max_orders):
    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            user_id = request.user.id 
            user_order_count = OrderOffer.objects.filter(user_id=user_id, offer_status=False).count()
            if user_order_count >= max_orders:
                return HttpResponse("Превышен лимит заказов. Максимальное количество заказов: {}".format(max_orders), status=400)
            return func(request, *args, **kwargs)
        return wrapped
    return decorator