from django.contrib import admin

from app.users.models import UserAccount, UserQuota, UserAgreement, UserAvatar


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "name", "is_active", "role"]

    fieldsets = (
        (
            "Личные данные",
            {
                "fields": (
                    "email",
                    "name",
                    "surname",
                    "person_telephone",
                    "person_address",
                )
            },
        ),
        (
            "Статусы",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "person_rating",
                    "role",
                    "notifications",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": tuple(
                    field.attname
                    for field in UserAccount._meta.fields
                    if field.attname not in ("person_created", "id")
                )
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


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
class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "color"]
