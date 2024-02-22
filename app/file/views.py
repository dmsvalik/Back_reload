from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from app.file.methods.file_work import TmpFileWork
from app.file import exception as ex
from .models import IpFileModel, FileModel
from .permissions import IpFileSizeLimit, IsFileOwner
from .serializers import FileModelSerializer, DeleteFileSerializer
from .swagger_documentation import file as swagger
from .tasks import task_delete_file
from .utils.helpers import get_client_ip


class CreateFileView(APIView):
    serializer_class = FileModelSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (AllowAny, IpFileSizeLimit)

    @swagger_auto_schema(**swagger.UploadFile.__dict__)
    def post(self, request, *args, **kwargs):
        file = request.FILES["upload_file"]
        tmp_file = TmpFileWork()
        try:
            save_data = tmp_file.create(file) or None
            file = tmp_file.save_file_db(**save_data)
            ip = get_client_ip(request)
            IpFileModel.objects.create(file=file, ip=ip)
            return Response(
                data={"file_id": file.id}, status=status.HTTP_201_CREATED
            )
        except (ex.ThisNotFileError, ex.FewElementsError):
            return Response(
                data={"message": "Ошибка при загрузке файла"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteFileView(APIView):
    serializer_class = DeleteFileSerializer
    permission_classes = (AllowAny, IsFileOwner | IsAdminUser)

    @swagger_auto_schema(**swagger.DeleteFile.__dict__)
    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_id = serializer.validated_data.get("file_id")
        file = FileModel.objects.get(id=file_id)
        file.delete()
        task_delete_file.delay(
            file_path=file.file_path,
            preview_path=file.preview_path,
            user_id=request.user.id or None,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
