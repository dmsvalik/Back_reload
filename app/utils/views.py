from celery.result import AsyncResult
from datetime import datetime, timedelta

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from app.products.models import Category

from drf_yasg.utils import swagger_auto_schema

from app.users.models import UserAccount, UserQuota
from app.orders.models import OrderModel, OrderOffer
from app.utils.permissions import IsContactor, IsFileExist, IsFileOwner
from app.utils.swagger_documentation.utils import AllDelete, DocsView

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

    user_quota = UserQuota.objects.get_or_create(user=user_account)[0]
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


@swagger_auto_schema(
    tags=DocsView.tags,
    operation_summary=DocsView.operation_summary,
    operation_description=DocsView.operation_description,
    manual_parameters=DocsView.manual_parameters,
    responses=DocsView.responses,
    method="get",
)
@api_view(('GET',))
@permission_classes([
    IsFileExist,
    IsAdminUser | IsContactor | IsFileOwner,
])
def document_view(request, path):
    """Возврат ссылки на превью картинки"""
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


class AllDeleteAPIView(viewsets.ViewSet, GenericAPIView):
# class AllDeleteAPIView(APIView):
    @permission_classes([IsAdminUser])
    @swagger_auto_schema(
        operation_description=AllDelete.operation_description,
        responses=AllDelete.responses,
        request_body=AllDelete.request_body,
        method="delete",
    )
    @action(detail=False, methods=['delete'])
    def delete_all_view(self, request):
        """
        Удаление ВСЕГО из БД кроме записи админа!!!!!!!!!!!"
        """
        try:
            OrderModel.objects.all().delete()
            Category.objects.all().delete()
            UserAccount.objects.filter(is_superuser=False).delete()
            return Response({'detail': 'Все записи, кроме админа, успешно удалены.'},
                            status=status.HTTP_204_NO_CONTENT)
        except OrderModel.DoesNotExist:
            return Response({'errors': 'Заказы не найдены.'}, status=status.HTTP_404_NOT_FOUND)
        except Category.DoesNotExist:
            return Response({'errors': 'Категории не найдены.'}, status=status.HTTP_404_NOT_FOUND)
        except UserAccount.DoesNotExist:
            return Response({'errors': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'errors': f'Не удалось удалить все записи: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
