from django.contrib import admin

from .models import (
    FileData,
    OrderFileData,
    OrderModel,
    OrderOffer,
    WorksheetFile,
)


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    """Админка заказа."""

    list_display = [
        "id",
        "name",
        "state",
        "user_account",
        "order_time",
    ]
    fields = [
        "name",
        "state",
        "user_account",
        "order_time",
        "key",
        "questionnaire_type",
    ]
    readonly_fields = ("order_time", "key")


@admin.register(OrderOffer)
class OrderOfferAdmin(admin.ModelAdmin):
    """Админка предложения."""

    list_display = ["offer_create_at", "id", "user_account", "order_id"]


@admin.register(FileData)
class FileDataAdmin(admin.ModelAdmin):
    """Админка для файлов пользователя."""

    list_display = ["id", "user_account", "order_id", "date_upload"]


@admin.register(OrderFileData)
class OrderFileDataAdmin(admin.ModelAdmin):
    """Админка для файлов заказа пользователя."""

    list_display = [
        "original_name",
        "order_id",
        "question_id",
        "date_upload",
    ]
    readonly_fields = ("id",)


@admin.register(WorksheetFile)
class WorksheetFile(admin.ModelAdmin):
    """Админка для генерации pdf файлов пользователя."""

    list_display = [
        "original_name",
        "order_id",
        "date_upload",
    ]
    readonly_fields = ("id",)
