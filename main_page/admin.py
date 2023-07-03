from django.contrib import admin

from .models import CooperationOffer, SellerData, UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["email", "id", "name", "is_active", "is_staff"]


@admin.register(SellerData)
class SellerDataAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "is_activ",
        "company_name",
        "phone_number",
        "requisites",
        "activity_type",
    ]


@admin.register(CooperationOffer)
class CooperationOfferAdmin(admin.ModelAdmin):
    list_display = ["user_account", "text", "created"]
