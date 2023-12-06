from celery.result import AsyncResult
from datetime import datetime, timedelta

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response

from app.users.models import UserQuota
from app.orders.models import OrderModel, OrderOffer
from app.utils.permissions import IsContactor, IsFileExist, IsFileOwner

from .serializers import GalleryImagesSerializer
from .models import GalleryImages


class GalleryImagesViewSet(viewsets.ModelViewSet):
    """
    Отображение картинок на главной странице в слайдерах

    """

    queryset = GalleryImages.objects.all()
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = GalleryImagesSerializer
    http_method_names = ["get"]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


def recalculate_quota(user_account, cloud_size, server_size):
    """
    Пересчитываем квоту пользователя

    """

    user_quota = UserQuota.objects.get(user=user_account)
    current_cloud_size = user_quota.total_cloud_size
    current_server_size = user_quota.total_server_size

    new_total_cloud_size = current_cloud_size + cloud_size
    new_total_server_size = current_server_size + server_size

    if new_total_cloud_size < 0:
        new_total_cloud_size = 0
    if new_total_server_size < 0:
        new_total_server_size = 0

    return UserQuota.objects.filter(user=user_account).update(
        total_cloud_size=new_total_cloud_size,
        total_server_size=new_total_server_size
    )


@api_view(["GET"])
def get_task_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
    }
    if result.get("task_status") == "SUCCESS" and task_result.result:
        result["task_status"] = task_result.result.get("status")
        result["response"] = task_result.result.get("response")

    return Response(result, status=200)


@api_view(('GET',))
@permission_classes([
    IsAuthenticated,
    IsFileExist,
    IsAdminUser | IsContactor | IsFileOwner,
])
def document_view(request, path):
    res = Response()
    res["X-Accel-Redirect"] = "/files/" + path
    return res


@api_view(('GET',))
def check_expired_auction_orders(request):
    """
    Проверка заказов в статусе аукциона

    """

    all_orders = OrderModel.objects.filter(state='auction')

    for item in all_orders:
        if datetime.now() > item.order_time.replace(tzinfo=None) + timedelta(days=1):
            check_offers = OrderOffer.objects.filter(order_id=item).count()
            if check_offers == 0:
                item.state = 'auction_expired_no_offers'
            else:
                item.state = 'auction_expired'
            item.save()

    # надо логи добавить сюда, что таска была запущена и завершилась или сделать отправку на почту
    return Response({'success': 'all orders auctions were checked'})
