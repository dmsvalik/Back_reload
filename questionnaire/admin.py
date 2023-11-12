from django.contrib import admin

from questionnaire.models import QuestionnaireCategory, QuestionnaireType, Question, Option, QuestionnaireChapter, \
    QuestionResponse


@admin.register(QuestionnaireCategory)
class QuestionnaireCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "category"]


@admin.register(QuestionnaireType)
class QuestionnaireTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "type", "description"]


@admin.register(QuestionnaireChapter)
class QuestionnaireChapterAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ["id", "name", "type"]
=======
    list_display = ["id", "name", "type", "get_quest_category"]

    @admin.display(description='Относится к Анкете', ordering='type_category')
    def get_quest_category(self, obj):
        return obj.type.category
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "chapter", "position", "option"]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "question"]


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "response", "order"]
