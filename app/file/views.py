from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from app.file.methods.offer import TmpFileWork
from .serializers import FileModelSerializer
from .swagger_documentation import file as swagger


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(**swagger.UploadFile.__dict__),
)
class FileView(CreateAPIView):
    serializer_class = FileModelSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        file = request.FILES["upload_file"]
        print(file.name)
        tmp_file = TmpFileWork()
        save_data = tmp_file.create(file)
        if save_data:
            file = tmp_file.save_file_db(**save_data)
            return Response(
                data={"file_id": file.id}, status=status.HTTP_201_CREATED
            )
