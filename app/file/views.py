from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from app.file.methods.offer import TmpFileWork
from .serializers import FileModelSerializer
from .swagger_documentation import file as swagger


class CreateFileView(APIView):
    serializer_class = FileModelSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = ()

    @swagger_auto_schema(**swagger.UploadFile.__dict__)
    def post(self, request, *args, **kwargs):
        file = request.FILES["upload_file"]
        tmp_file = TmpFileWork()
        save_data = tmp_file.create(file) or None
        if save_data:
            file = tmp_file.save_file_db(**save_data)
            return Response(
                data={"file_id": file.id}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data={"message": "Ошибка при загрузке файла"},
                status=status.HTTP_400_BAD_REQUEST,
            )
