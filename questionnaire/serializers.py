from rest_framework import serializers

from questionnaire.models import QuestionnaireCategory, QuestionnaireType, Question, Option, QuestionnaireChapter


class QuestionnaireCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireCategory
        fields = ["id", "name"]


class OptionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ["id", "text", "option_type", "questions"]

    def get_questions(self, obj):
        queryset = Question.objects.filter(option=obj).order_by("position")
        serializer = QuestionSerializer(queryset, read_only=True, many=True)
        return serializer.data


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ["id", "text", "answer_type", "file_required", "options"]

    def get_options(self, obj):
        queryset = Option.objects.filter(question=obj)
        serializer = OptionSerializer(queryset, read_only=True, many=True)
        return serializer.data


class QuestionnaireChapterSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = QuestionnaireChapter
        fields = ["id", "name", "questions"]

    def get_questions(self, obj):
        queryset = Question.objects.filter(chapter=obj, option__isnull=True).order_by("position")
        serializer = QuestionSerializer(queryset, read_only=True, many=True)
        return serializer.data


class QuestionnaireTypeSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuestionnaireType
        fields = ["id", "type", "description", "chapters"]

    def get_chapters(self, obj):
        queryset = QuestionnaireChapter.objects.filter(type=obj)
        serializer = QuestionnaireChapterSerializer(queryset, read_only=True, many=True)
        return serializer.data
