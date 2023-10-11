from django.contrib import admin
from .models import OrderModel, OrderOffer, FileData


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["order_time", "id", "state", "user_account"]


@admin.register(OrderOffer)
class OrderOfferAdmin(admin.ModelAdmin):
    list_display = ["offer_create_at", "id", "order_id"]


@admin.register(FileData)
class FileDataAdmin(admin.ModelAdmin):
    list_display = ["id", "user_account", "order_id", "date_upload"]
