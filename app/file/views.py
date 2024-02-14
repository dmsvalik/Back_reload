# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.file.methods.offer import TmpFileWork


class FileView(APIView):
    serializer_class = None

    def post(self, request, *args, **kwargs):
        file = request.FILES["upload_file"]
        tmp_file = TmpFileWork()
        save_data = tmp_file.create(file)
        if save_data:
            file = tmp_file.save_file_db(**save_data)
            return Response(
                data={"file_id": file.id}, status=status.HTTP_201_CREATED
            )
