from django.contrib import admin

from app.questionnaire.models import (
    QuestionnaireType,
    Question,
    Option,
    QuestionnaireChapter,
    QuestionResponse,
)


@admin.register(QuestionnaireType)
class QuestionnaireTypeAdmin(admin.ModelAdmin):
    """Админка для типа анкеты."""

    list_display = ["id", "category", "type", "description", "active"]


@admin.register(QuestionnaireChapter)
class QuestionnaireChapterAdmin(admin.ModelAdmin):
    """Админка для разделов анкеты."""

    list_display = ["id", "name", "type", "get_quest_category"]

    @admin.display(description="Относится к Анкете", ordering="type_category")
    def get_quest_category(self, obj):
        return obj.type.category


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Админка для вопросов анкеты."""

    list_display = ["id", "text", "chapter", "position", "option"]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    """Админка для вариантов ответа."""

    list_display = ["id", "text", "question"]


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    """Админка для ответов на вопросы."""

    list_display = ["id", "question", "response", "order"]
