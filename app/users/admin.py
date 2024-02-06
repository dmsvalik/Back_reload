from django.contrib import admin

from app.users.models import UserAccount, UserQuota, UserAgreement, UserAvatar


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "name", "is_active", "role"]


@admin.register(UserQuota)
class UserQuotaAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "total_cloud_size",
        "total_server_size",
        "total_traffic",
    ]


@admin.register(UserAgreement)
class UserAgreementAdmin(admin.ModelAdmin):
    list_display = ["id", "user_account", "date"]


@admin.register(UserAvatar)
class UserAgreementAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "color"]
