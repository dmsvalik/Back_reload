from django.contrib import admin

from .models import FileData, OrderFileData, OrderModel, OrderOffer


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "state", "user_account", "order_time", ]
    fields = ["name", "state", "user_account", "order_time", "key", ]
    readonly_fields = ("order_time", "key")


@admin.register(OrderOffer)
class OrderOfferAdmin(admin.ModelAdmin):
    list_display = ["offer_create_at", "id", "user_account", "order_id"]


@admin.register(FileData)
class FileDataAdmin(admin.ModelAdmin):
    list_display = ["id", "user_account", "order_id", "date_upload"]


@admin.register(OrderFileData)
class OrderFileDataAdmin(admin.ModelAdmin):
    list_display = ["id", "original_name", "order_id", "question_id", "date_upload"]
