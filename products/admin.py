from django.contrib import admin

from .models import CardModel, CategoryModel


@admin.register(CardModel)
class CardModelAdmin(admin.ModelAdmin):
    list_display = ['card_name']


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['category_name']
