from django.contrib import admin
from .models import OrderModel, OrderImageModel


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['order_time', 'id', 'state', 'user_account']

@admin.register(OrderImageModel)
class OrderImageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id']
