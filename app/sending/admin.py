from django.contrib import admin

from app.sending.models import UserNotifications, SentNotification


@admin.register(UserNotifications)
class UserNotificationsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "notification_type"]


@admin.register(SentNotification)
class SentNotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at", "theme", "type"]
