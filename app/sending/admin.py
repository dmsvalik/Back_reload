from django.contrib import admin

from app.sending.models import UserNotifications


@admin.register(UserNotifications)
class UserNotificationsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "notification_type"]
