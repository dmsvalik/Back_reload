from datetime import timedelta, datetime

from rest_framework import permissions
from rest_framework.exceptions import ValidationError


class ChangePriceInOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.data.get('offer_price'):
            if request.method in ('POST'):
                return ValidationError('Цену можно указать через день после размещения заказа')
            if request.method in ('PATH', 'PUT'):
                if datetime.now() < obj.order_id.order_time + timedelta(days=1):
                    return ValidationError('Цену можно указать через день после размещения заказа')
        return True
