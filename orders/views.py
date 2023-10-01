import mimetypes

from utils import errorcode
from utils.decorators import check_file_type, check_user_quota
from utils.storage import CloudStorage

# from django.core.cache import caches
from django.core.files.temp import NamedTemporaryFile
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ImageData, OrderImageModel, OrderOffer
from .permissions import ChangePriceInOrder
from .serializers import OrderImageSerializer, OrderOfferSerializer
from main_page.permissions import IsSeller


class OrderImageViewSet(viewsets.ModelViewSet):
    """Проверка картинок по продукту + создание картинок с привязкой к продукту - test"""

    permission_classes = [IsAuthenticated]
    queryset = OrderImageModel.objects.all()
    serializer_class = OrderImageSerializer

    # достаем все объекты пользователя
    def get_queryset(self):
        user = self.request.user
        return OrderImageModel.objects.filter(order_id__user_account=user)


class OrderOfferViewSet(viewsets.ModelViewSet):
    """Поведение Оффера"""

    permission_classes = [IsAuthenticated, IsSeller, ChangePriceInOrder]
    queryset = OrderOffer.objects.all()
    serializer_class = OrderOfferSerializer

    # достаем все объекты пользователя
    def get_queryset(self):
        user = self.request.user
        return OrderOffer.objects.filter(user_account=user)


@api_view(["POST"])
@check_file_type(
    [
        "jpg",
    ]
)
@check_user_quota
def upload_image_order(request):
    """
    Процесс приема изображения и последующего сохранения

    """
    order_id = request.POST.get("order_id")
    image = request.FILES["upload_file"]
    user_id = request.user.id
    name = image.name

    if order_id == "" or not order_id.isdigit():
        raise errorcode.IncorrectImageOrderUpload()

    # save temp version of the file in system, for celery task
    temp_file = NamedTemporaryFile(delete=True)
    for block in image.chunks():
        temp_file.write(block)
    temp_file.flush()

    yandex = CloudStorage()
    response_code, yandex_path = yandex.cloud_upload_image(
        temp_file.name, user_id, order_id, name
    )
    temp_file.close()

    if response_code == 201:
        ImageData.objects.create(
            user_account=request.user, yandex_path=yandex_path, order_id=order_id
        )  # TODO
        return Response({"status": "success"})
    return Response(
        {
            "status": "failed",
            "message": f"Unexpected response from Yandex.Disk: {response_code}",
        },
    )


# file_cache = caches["file_cache"]


@api_view(["GET"])
def get_image_order(request, id):
    """
    Получение изображения и передача его на фронт
    """

    # Поиск пути изображения в БД по ID
    image_data = get_object_or_404(
        ImageData, id=id
    )  # TODO: Добавить логику ошибки в errorcode.py

    yandex_path = image_data.yandex_path

    # Иначе получаем изображение из Yandex
    yandex = CloudStorage()
    try:
        image_data = yandex.cloud_get_image(yandex_path)
    except Exception as e:
        return Response(
            {
                "status": "failed",
                "message": f"Failed to get image from Yandex.Disk: {str(e)}",
            },
        )

    # Сохраняем изображение в кеш
    # file_cache.set(yandex_path, image_data)

    # передача изображения на фронт
    # Обработка различных форматов файлов, определяем MIME-тип динамически на основе расширения файла
    mime_type, encoding = mimetypes.guess_type(yandex_path.split("/")[-1])
    response = FileResponse(
        image_data, content_type=mime_type if mime_type else "application/octet-stream"
    )
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{yandex_path.split("/")[-1]}"'
    return response


# TODO: Для проверки файла при POST и GET запросах...?
# def check_file_type(allowed_types):
#     def decorator(func):
#         @wraps(func)
#         def wrapped(request, *args, **kwargs):
#             if request.method == 'POST':
#                 uploaded_file = request.FILES.get('upload_file')
#                 if "upload_file" not in request.FILES:
#                     return HttpResponse(
#                         {'The "upload_file" key is missing in the uploaded files.'}, status=400
#                     )
#                 else:
#                     file_extension = uploaded_file.name.split('.')[-1].lower()
#                     if file_extension not in allowed_types:
#                         return HttpResponse("Invalid file type.", status=400)
#             elif request.method == 'GET':
#                 id = kwargs.get('id')
#                 image_data = get_object_or_404(ImageData, id=id)
#                 file_extension = image_data.yandex_path.split('.')[-1].lower()
#                 if file_extension not in allowed_types:
#                     return HttpResponse("Invalid file type.", status=400)
#             return func(request, *args, **kwargs)
#         return wrapped
#     return decorator
