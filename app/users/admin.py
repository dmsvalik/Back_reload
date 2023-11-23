from django.contrib import admin

from app.users.models import UserAccount, EmailSendTime, UserQuota, UserAgreement


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["email", "id", "name", "is_active", "role"]


@admin.register(EmailSendTime)
class EmailSendTimeAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "timestamp"]


@admin.register(UserQuota)
class UserQuotaAdmin(admin.ModelAdmin):
    list_display = ["user", "total_cloud_size", "total_server_size", "total_traffic"]

@admin.register(UserAgreement)
class UserAgreementAdmin(admin.ModelAdmin):
    list_display = ["user_account", "date"]
