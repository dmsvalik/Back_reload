from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка категорий."""

    list_display = ["id", "name", "active"]
