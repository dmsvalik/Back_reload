from django.contrib import admin

from app.questionnaire.models import QuestionnaireCategory, QuestionnaireType, Question, Option, QuestionnaireChapter, \
    QuestionResponse


@admin.register(QuestionnaireCategory)
class QuestionnaireCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "category"]


@admin.register(QuestionnaireType)
class QuestionnaireTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "type", "description", "active"]


@admin.register(QuestionnaireChapter)
class QuestionnaireChapterAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type", "get_quest_category"]

    @admin.display(description='Относится к Анкете', ordering='type_category')
    def get_quest_category(self, obj):
        return obj.type.category


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "chapter", "position", "option"]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "question"]


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "response", "order"]
