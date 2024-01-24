from uuid import UUID

from celery.result import AsyncResult
from datetime import datetime, timedelta

from django.http import HttpResponseNotFound
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from app.products.models import Category
from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from app.users.models import UserAccount
from app.orders.models import OrderModel, OrderOffer, OrderFileData
from app.utils.swagger_documentation import utils as swagger
from app.utils.tasks import celery_get_order_pdf
from . import errorcode

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
        AllowAny,
    ]
)
def document_view(request, file_id: UUID):
    """Возврат ссылки на превью картинки. Редиректит
    на превью.
    URL: http://localhost/documents/<file_id>/
    METHOD - "GET"
    file_id:str (обязательное) - id файла"""

    try:
        UUID(str(file_id))
    except ValueError:
        raise errorcode.FileNotFound()
    file_models = (OrderFileData,)
    file = None
    for file_model in file_models:
        file = file_model.objects.filter(id=file_id).first()
        if file:
            break
    if not file:
        raise errorcode.FileNotFound()
    res = Response()
    res["X-Accel-Redirect"] = "/files/" + file.server_path
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


#
# def draw_order_pdf(items, order_id) -> str:
#     """Function for drawing pdf file"""
#     output_pdf = os.path.join(PDF_DIR, f"output_pdf{order_id}.pdf")
#     pdf = SimpleDocTemplate(output_pdf)
#     flow_obj = []
#     styles = getSampleStyleSheet()
#     styles["Title"].fontName = "Montserrat-Medium"
#     styles["Normal"].fontName = "Montserrat-Medium"
#     styles["Heading1"].fontName = "Montserrat-Medium"
#     styles["Heading2"].fontName = "Montserrat-Medium"
#     pdfmetrics.registerFont(TTFont("Montserrat-Medium", ttf_file))
#     title = Paragraph("Ваш заказ", styles["Title"])
#     flow_obj.append(title)
#     order = items["order"]
#     description = Paragraph(f"{order.order_description}", styles["Heading2"])
#     flow_obj.append(description)
#     for i, question in enumerate(items["questions"], 1):
#         flow_obj.append(
#             Paragraph(
#                 f"{i}) {question.text}",
#                 style=styles["Normal"],
#             )
#         )
#         response = question.questionresponse_set.filter(order=order).first()
#         if response:
#             flow_obj.append(
#                 Paragraph(
#                     f"- {response.response}",
#                     style=styles["Normal"],
#                 )
#             )
#         files = question.orderfiledata_set.filter(order_id=order)
#         if files:
#             for file in files:
#                 filedata = Paragraph(
#                     f""" <a href={file.server_path}> -
#                                 <u>{file.original_name}</u></a> """,
#                     style=styles["Normal"],
#                 )
#                 flow_obj.append(filedata)
#         flow_obj.append(Spacer(10, 6))
#     pdf.build(flow_obj)
#     new_pdf = PdfReader(output_pdf)
#     output = PdfWriter()
#     for page in new_pdf.pages:
#         existing_pdf = PdfReader(open(design_pdf, "rb"))
#         design_page = existing_pdf.pages[0]
#         design_page.merge_page(page)
#         output.add_page(design_page)
#     output_stream = open(output_pdf, "wb")
#     output.write(output_stream)
#     output_stream.close()
#     return output_pdf
#
#


@swagger_auto_schema(**swagger.GetOrderPdf.__dict__)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_order_pdf(request, pk) -> Response | HttpResponseNotFound:
    """Return pdf file"""
    try:
        task = celery_get_order_pdf(pk)
        return Response({"task_id": task.id})
    except AttributeError:
        return HttpResponseNotFound("Такого заказа не существует")

    # try:
    #     item = OrderModel.objects.filter(id=pk).first()
    #     question_id_with_answer = list(
    #         item.questionresponse_set.values_list("question_id", flat=True)
    #     )
    #     question_id_with_files = list(
    #         item.orderfiledata_set.values_list("question_id_id", flat=True)
    #     )
    #     all_questions = Question.objects.filter(
    #         chapter__type=item.questionnaire_type
    #     )
    #     queryset = all_questions.filter(
    #         id__in=set(question_id_with_answer + question_id_with_files)
    #     )
    #     items = {"order": item, "questions": queryset}
    #     response = FileResponse(
    #         open(draw_order_pdf(items, pk), "rb"),
    #         as_attachment=True,
    #         content_type="application/pdf",
    #     )
    #     return response
    # except AttributeError:
    #     return HttpResponseNotFound("Такого заказа не существует")
