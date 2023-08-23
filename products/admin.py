from django.contrib import admin
from .models import (CardModel, CategoryModel, QuestionOptionsModel, QuestionsProductsModel, ResponseModel)


@admin.register(CardModel)
class CardModelAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(QuestionsProductsModel)
class QuestionsProductsModelAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "position", "category_id"]
    search_fields = (
        "id",
        "question",
    )
    list_filter = (("category_id"),)


@admin.register(QuestionOptionsModel)
class QuestionOptionsModelAdmin(admin.ModelAdmin):
    list_display = ["question", "option"]
    autocomplete_fields = ["question"]


@admin.register(ResponseModel)
class ResponseModelAdmin(admin.ModelAdmin):
    list_display = ["id", "order_id", "question", "user_account", "response"]
    search_fields = (
        "user_account",
        "id_question",
    )
