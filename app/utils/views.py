import os

from celery.result import AsyncResult
from datetime import datetime, timedelta

from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from django.http import FileResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from app.products.models import Category
from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from app.users.models import UserAccount
from app.orders.models import OrderModel, OrderOffer
from app.utils.permissions import IsContactor, IsFileExist, IsFileOwner
from app.utils.swagger_documentation import utils as swagger
from config.settings import ttf_file, design_pdf, PDF_DIR


from .serializers import GalleryImagesSerializer
from .models import GalleryImages


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(**swagger.GalleryImagesList.__dict__),
)
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


@swagger_auto_schema(**swagger.GetTaskStatus.__dict__)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_task_status(request, task_id):
    """
    Получение статуса таски CELERY. task_id - идентификатор таски.
    Статусы: SUCCESS, FAILURE
    Для отображения статуса необходимо отправить в result
    "task_id"и "task_status"
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
    }
    if result.get("task_status") == "SUCCESS" and task_result.result:
        result["task_status"] = task_result.result.get("status")
        result["response"] = task_result.result.get("response")

    return Response(result, status=200)


@swagger_auto_schema(**swagger.DocsView.__dict__)
@api_view(("GET",))
@permission_classes(
    [
        IsFileExist,
        IsAdminUser | IsContactor | IsFileOwner,
    ]
)
def document_view(request, path):
    """Возврат ссылки на превью картинки. Проверяет доступ и редиректит
    на превью."""
    res = Response()
    res["X-Accel-Redirect"] = "/files/" + path
    return res


@swagger_auto_schema(**swagger.CheckExpAuctionOrdersDocs.__dict__)
@api_view(("GET",))
def check_expired_auction_orders(request):
    """
    Проверка заказов в статусе аукциона

    """

    all_orders = OrderModel.objects.filter(state="auction")

    for item in all_orders:
        if datetime.now() > item.order_time.replace(tzinfo=None) + timedelta(
            days=1
        ):
            check_offers = OrderOffer.objects.filter(order_id=item).count()
            if check_offers == 0:
                item.state = "auction_expired_no_offers"
            else:
                item.state = "auction_expired"
            item.save()

    # надо логи добавить сюда, что таска была запущена и завершилась или
    # сделать отправку на почту
    return Response({"success": "all orders auctions were checked"})


class AllDeleteAPIView(viewsets.ViewSet, GenericAPIView):
    # class AllDeleteAPIView(APIView):
    @permission_classes([IsAdminUser])
    @swagger_auto_schema(**swagger.AllDelete.__dict__)
    @action(detail=False, methods=["delete"])
    def delete_all_view(self, request):
        """
        Удаление ВСЕГО из БД кроме записи админа!!!!!!!!!!!"
        """
        try:
            OrderModel.objects.all().delete()
            Category.objects.all().delete()
            UserAccount.objects.filter(is_superuser=False).delete()
            return Response(
                {"detail": "Все записи, кроме админа, успешно удалены."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except OrderModel.DoesNotExist:
            return Response(
                {"errors": "Заказы не найдены."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Category.DoesNotExist:
            return Response(
                {"errors": "Категории не найдены."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except UserAccount.DoesNotExist:
            return Response(
                {"errors": "Пользователь не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"errors": f"Не удалось удалить все записи: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def draw_order_pdf(items, order_id) -> str:
    """Function for drawing pdf file"""
    output_pdf = os.path.join(PDF_DIR, f"output_pdf{order_id}.pdf")
    pdf = SimpleDocTemplate(output_pdf)
    flow_obj = []
    styles = getSampleStyleSheet()
    styles["Title"].fontName = "Montserrat-Medium"
    styles["Normal"].fontName = "Montserrat-Medium"
    styles["Heading1"].fontName = "Montserrat-Medium"
    styles["Heading2"].fontName = "Montserrat-Medium"
    pdfmetrics.registerFont(TTFont("Montserrat-Medium", ttf_file))
    title = Paragraph("Ваш заказ", styles["Title"])
    flow_obj.append(title)
    name = Paragraph(
        f'{items[0]["user_account__ordermodel__name"]}', styles["Heading1"]
    )
    flow_obj.append(name)
    description = Paragraph(
        f'{items[1]["order_description"]}', styles["Heading2"]
    )
    flow_obj.append(description)
    for i, item in enumerate(items, 1):
        flow_obj.append(
            Paragraph(
                f'{i}) {item["questionresponse__question__text"]}',
                style=styles["Normal"],
            )
        )
        flow_obj.append(
            Paragraph(
                f'- {item["questionresponse__response"]}',
                style=styles["Normal"],
            )
        )
        flow_obj.append(
            Paragraph(
                f""" <a href={item["orderfiledata__server_path"]}> -
                        <u>{item["orderfiledata__original_name"]}</u></a> """,
                style=styles["Normal"],
            )
        )
    pdf.build(flow_obj)
    new_pdf = PdfReader(output_pdf)
    existing_pdf = PdfReader(open(design_pdf, "rb"))
    output = PdfWriter()
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    output_stream = open(output_pdf, "wb")
    output.write(output_stream)
    output_stream.close()
    return output_pdf


@api_view(["GET"])
def get_order_pdf(request, order_id) -> Response | FileResponse:
    """Return pdf file"""
    user = request.user
    if not OrderModel.objects.filter(user_account=user).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    items = OrderModel.objects.filter(id=order_id)
    items = items.values(
        "user_account__ordermodel__name",
        "order_description",
        "questionresponse__response",
        "questionresponse__question__text",
        "orderfiledata__server_path",
        "orderfiledata__original_name",
    )
    return FileResponse(
        open(draw_order_pdf(items, order_id), "rb"),
        content_type="application/pdf",
    )
