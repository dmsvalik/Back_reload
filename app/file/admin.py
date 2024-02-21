from django.contrib import admin

from app.file.models import OfferFileModel, FileModel, IpFileModel


@admin.register(FileModel)
class FileModelAdmin(admin.ModelAdmin):
    """Админка для файлов заказа пользователя."""

    list_display = [
        "id",
        "original_name",
        "date_upload",
    ]
    readonly_fields = ("id",)
    ordering = ["-date_upload"]


@admin.register(OfferFileModel)
class OfferFileModelAdmin(admin.ModelAdmin):
    """Админка для файлов оффера."""

    list_display = [
        "id",
        "file",
        "offer",
        "date_upload",
    ]

    def date_upload(self, obj):
        return obj.file.date_upload


@admin.register(IpFileModel)
class IpFileModelAdmin(admin.ModelAdmin):
    """Админка для файлов заказа пользователя."""

    list_display = [
        "id",
        "ip",
        "file",
    ]
    readonly_fields = ("id",)
