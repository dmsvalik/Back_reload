from django.contrib import admin

from .models import CooperationOffer, UserAccount, EmailSendTime, ContactSupport
from .models import ContractorData
from main_page.models import UserQuota


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["email", "id", "name", "is_active", "is_staff"]


@admin.register(ContractorData)
class ContractorDataAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "is_active",
        "company_name",
        "phone_number",
        "requisites",
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
    list_display = ["user", "total_cloud_size", "total_server_size", "total_traffic"]
