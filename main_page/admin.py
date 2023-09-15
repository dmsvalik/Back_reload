from django.contrib import admin

from .models import CooperationOffer, SellerData, UserAccount, EmailSendTime, ContactSupport

from utils.models import UserQuota


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


@admin.register(ContactSupport)
class ContactSupportAdmin(admin.ModelAdmin):
    list_display = ["user_account", "user_question", "created"]


@admin.register(CooperationOffer)
class CooperationOfferAdmin(admin.ModelAdmin):
    list_display = ["user_account", "text", "created"]


@admin.register(EmailSendTime)
class EmailSendTimeAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "timestamp"]

@admin.register(UserQuota)
class UserQuotaAdmin(admin.ModelAdmin):
    list_display = ["user", "quota_cloud_size", "total_server_size", "total_traffic"]
