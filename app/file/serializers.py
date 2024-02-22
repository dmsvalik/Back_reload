from rest_framework import serializers

from app.file.models import FileModel, OfferFileModel
from config import settings


class FileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ("id",)
        read_only_fields = ("id",)


class DeleteFileSerializer(serializers.Serializer):
    file_id = serializers.PrimaryKeyRelatedField(
        queryset=FileModel.objects.all(), source="file.id"
    )

    class Meta:
        fields = ("file_id",)


class OfferFileWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=FileModel.objects.all(), source="file.id"
    )
    original_name = serializers.ReadOnlyField(source="file.original_name")
    size = serializers.ReadOnlyField(source="file.server_size")

    class Meta:
        model = OfferFileModel
        fields = ("id", "original_name", "size")


class FilesSerializer(serializers.ModelSerializer):
    """Сериализатор для файлов пользователя"""

    file_size = serializers.IntegerField(source="server_size")
    preview_url = serializers.SerializerMethodField()

    class Meta:
        model = FileModel
        fields = ["id", "original_name", "file_size", "preview_url"]

    def get_preview_url(self, order_file_data_obj):
        """
        Generate preview_url field for url path to preview
        """
        if not order_file_data_obj.preview_path:
            return None
        preview = "https://{domain}/documents/{file_id}/"
        return preview.format(
            domain=settings.DOMAIN, file_id=order_file_data_obj.id
        )
