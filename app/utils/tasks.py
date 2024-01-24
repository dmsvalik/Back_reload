import os

from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from rest_framework import status
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.utils.storage import CloudStorage
from config.settings import ttf_file, design_pdf, BASE_DIR

from app.orders.models import OrderModel, WorksheetFile
from app.questionnaire.models import Question

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def draw_order_pdf(items: dict, order_id: int, user_id: int) -> str:
    """Function for drawing pdf file"""

    output_pdf = os.path.join(
        BASE_DIR,
        "media",
        str(user_id),
        str(order_id),
        f"worksheet_{order_id}.pdf",
    )
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
    order = items["order"]
    description = Paragraph(f"{order.order_description}", styles["Heading2"])
    flow_obj.append(description)
    for i, question in enumerate(items["questions"], 1):
        flow_obj.append(
            Paragraph(
                f"{i}) {question.text}",
                style=styles["Normal"],
            )
        )
        response = question.questionresponse_set.filter(order=order).first()
        if response:
            flow_obj.append(
                Paragraph(
                    f"- {response.response}",
                    style=styles["Normal"],
                )
            )
        files = question.orderfiledata_set.filter(order_id=order)
        if files:
            for file in files:
                filedata = Paragraph(
                    f""" <a href={file.server_path}> -
                                <u>{file.original_name}</u></a> """,
                    style=styles["Normal"],
                )
                flow_obj.append(filedata)
        flow_obj.append(Spacer(10, 6))
    pdf.build(flow_obj)
    new_pdf = PdfReader(output_pdf)
    output = PdfWriter()
    for page in new_pdf.pages:
        existing_pdf = PdfReader(open(design_pdf, "rb"))
        design_page = existing_pdf.pages[0]
        design_page.merge_page(page)
        output.add_page(design_page)
    output_stream = open(output_pdf, "wb")
    output.write(output_stream)
    output_stream.close()
    return output_pdf


@shared_task()
def celery_get_order_pdf(order_id):
    """Return pdf file"""
    try:
        item = OrderModel.objects.filter(id=order_id).first()
        user = item.user_account
        question_id_with_answer = list(
            item.questionresponse_set.values_list("question_id", flat=True)
        )
        question_id_with_files = list(
            item.orderfiledata_set.values_list("question_id_id", flat=True)
        )
        all_questions = Question.objects.filter(
            chapter__type=item.questionnaire_type
        )
        queryset = all_questions.filter(
            id__in=set(question_id_with_answer + question_id_with_files)
        )
        items = {"order": item, "questions": queryset}
        output_pdf = draw_order_pdf(items, order_id, user.id)
        file_name = output_pdf.split("/")[-1]
        worksheet = WorksheetFile.objects.create(
            order_id=order_id,
            original_name=file_name,
            server_path=f"{user.id}/{order_id}/{file_name}",
        )
        yandex = CloudStorage()
        result = yandex.cloud_upload_image(
            output_pdf, user.id, order_id, file_name
        )
        if result["status_code"] == status.HTTP_201_CREATED:
            worksheet.yandex_path = f"{user.id}/{order_id}/{file_name}"
            if os.path.exists(output_pdf):
                os.remove(output_pdf)
                worksheet.server_path = ""
            worksheet.save()
        return {"status": "SUCCESS", "response": "Файл создан"}
    except AttributeError:
        return logger.error(f"Заказ с номером {order_id} не найден")
