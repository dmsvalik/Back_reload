from rest_framework import serializers

from app.file.models import FileModel


class FileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ("id",)
        read_only_fields = ("id",)
