from django.contrib import admin

from questionnaire.models import QuestionnaireCategory, QuestionnaireType, Question, Options, QuestionnaireChapter, \
    QuestionResponse


@admin.register(QuestionnaireCategory)
class QuestionnaireCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "card_id"]


@admin.register(QuestionnaireType)
class QuestionnaireTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "questionnaire_category", "questionnaire_type", "description"]


@admin.register(QuestionnaireChapter)
class QuestionnaireChapterAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "questionnaire_type"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "questionnaire_chapter", "option"]


@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "question"]


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "response", "order_id"]
