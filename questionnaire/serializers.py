from rest_framework import serializers

from questionnaire.models import QuestionnaireCategory, QuestionnaireType, Question, Options, QuestionnaireChapter


class QuestionnaireCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireCategory
        fields = ["id", "name"]


class OptionsSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Options
        fields = ["id", "text", "option_type", "file_required", "questions"]

    def get_questions(self, obj):
        queryset = Question.objects.filter(option=obj)
        serializer = QuestionSerializer(queryset, read_only=True, many=True)
        return serializer.data


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ["id", "text", "answer_type", "file_required", "options"]

    def get_options(self, obj):
        queryset = Options.objects.filter(question=obj)
        serializer = OptionsSerializer(queryset, read_only=True, many=True)
        return serializer.data


class QuestionnaireChapterSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = QuestionnaireChapter
        fields = ["id", "name", "questions"]

    def get_questions(self, obj):
        queryset = Question.objects.filter(questionnaire_chapter=obj, option__isnull=True)
        serializer = QuestionSerializer(queryset, read_only=True, many=True)
        return serializer.data


class QuestionnaireTypeSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuestionnaireType
        fields = ["id", "questionnaire_type", "description", "chapters"]


    def get_chapters(self, obj):
        queryset = QuestionnaireChapter.objects.filter(questionnaire_type=obj)
        serializer = QuestionnaireChapterSerializer(queryset, read_only=True, many=True)
        return serializer.data
