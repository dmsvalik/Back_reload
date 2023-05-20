from django.contrib import admin
from .models import OrderModel


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['order_time', 'id', 'state', 'user_account']