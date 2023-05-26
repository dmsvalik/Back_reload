from django.contrib import admin
from .models import CardModel, CategoryModel, ProductModel, QuestionsProductsModel, ResponseModel, \
    QuestionOptionsKitchenModel
from django.contrib.admin import RelatedFieldListFilter


@admin.register(CardModel)
class CardModelAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_account', 'product_description', 'product_price']


@admin.register(QuestionsProductsModel)
class QuestionsProductsModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'position', 'category_id']
    search_fields = (
        'position',
    )
    list_filter = (
        ('category_id'),
    )


@admin.register(QuestionOptionsKitchenModel)
class QuestionOptionsKitchenModelAdmin(admin.ModelAdmin):

    list_display = ['question_id', 'option']


@admin.register(ResponseModel)
class ResponseModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_question', 'user_account', 'response']
    search_fields = (
        'user_account',
        'id_question',
    )

