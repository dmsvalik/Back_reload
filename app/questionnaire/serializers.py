from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings

from app.orders.models import OrderModel, OrderFileData
from app.questionnaire.models import (
    QuestionnaireType,
    Question,
    Option,
    QuestionnaireChapter,
    QuestionResponse,
)

from .utils.helpers import get_nested_questions


class OrderedByPositionSerializer(serializers.ListSerializer):
    """Сортировка по позициям."""

    def to_representation(self, data):
        data = data.order_by("position")
        return super(OrderedByPositionSerializer, self).to_representation(data)


class FirstLevelQuestionsSerializer(serializers.ListSerializer):
    """Сортировка первого уровня вопросов по позициям."""

    def to_representation(self, data):
        data = data.filter(option__isnull=True).order_by("position")
        return super(FirstLevelQuestionsSerializer, self).to_representation(
            data
        )


class FileSerializer(serializers.ModelSerializer):
    """Сериализатор для файлов пользователя приложенных к вопросам анкеты."""

    file_size = serializers.IntegerField(source="yandex_size")
    preview_url = serializers.SerializerMethodField()

    class Meta:
        model = OrderFileData
        fields = ["id", "original_name", "file_size", "preview_url"]

    def get_preview_url(self, order_file_data_obj):
        """
        Generate preview_url field for url path to preview
        """
        if not order_file_data_obj.server_path:
            return None
        preview = "https://{domain}/documents/{server_path}"
        return preview.format(
            domain=settings.DOMAIN, server_path=order_file_data_obj.server_path
        )


class QuestionResponseSerializer(serializers.ModelSerializer):
    """Сериализвтор ответов на вопросы."""

    files = serializers.SerializerMethodField(required=False)
    question_id = serializers.IntegerField(
        source="question.id", read_only=True
    )

    class Meta:
        model = QuestionResponse
        fields = ["id", "question_id", "response", "files"]

    def get_files(self, question_response: QuestionResponse):
        files = OrderFileData.objects.filter(
            order_id=question_response.order,
            question_id=question_response.question,
        )
        return FileSerializer(instance=files, many=True).data


class OptionSerializer(serializers.ModelSerializer):
    """Сериализатор вариантов ответов с вложенными вопросами."""

    questions = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ["id", "text", "option_type", "questions"]

    def get_questions(self, obj):
        queryset = Question.objects.filter(option=obj).order_by("position")
        serializer = QuestionSerializer(queryset, read_only=True, many=True)
        return serializer.data


class OuterQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор вопросов 1 уровня (не ссылающихся на варианты ответов)."""

    options = OptionSerializer(
        read_only=True, many=True, source="question_parent"
    )

    class Meta:
        model = Question
        list_serializer_class = FirstLevelQuestionsSerializer
        fields = [
            "id",
            "text",
            "answer_type",
            "file_required",
            "answer_required",
            "options",
        ]


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор вложенных вопросов."""

    options = OptionSerializer(
        read_only=True, many=True, source="question_parent"
    )

    class Meta:
        model = Question
        list_serializer_class = OrderedByPositionSerializer
        fields = [
            "id",
            "text",
            "answer_type",
            "file_required",
            "answer_required",
            "options",
        ]


class QuestionnaireChapterSerializer(serializers.ModelSerializer):
    """Сериализатор разделов анкеты."""

    questions = OuterQuestionSerializer(
        read_only=True, many=True, source="question_set"
    )

    class Meta:
        model = QuestionnaireChapter
        list_serializer_class = OrderedByPositionSerializer
        fields = ["id", "name", "questions"]


class QuestionnaireTypeSerializer(serializers.ModelSerializer):
    """Сериализатор типа анкеты с разделами."""

    chapters = QuestionnaireChapterSerializer(
        read_only=True, many=True, source="questionnairechapter_set"
    )

    class Meta:
        model = QuestionnaireType
        fields = ["id", "type", "description", "chapters"]


class QuestionnaireResponseSerializer(serializers.ModelSerializer):
    """Сериализатор ответов на анкету."""

    question_id = serializers.PrimaryKeyRelatedField(
        source="question", queryset=Question.objects.all()
    )

    class Meta:
        model = QuestionResponse
        fields = ["id", "question_id", "response"]
        read_only_fields = ["id", "order"]

    def validate(self, data):
        """
        Валидация ответа на вопрос.
        Вопрос должен соответствовать типу анкеты.
        При доступности вариантов ответов на вопросы. Ответ должен
        соответствовать одному из них
        """
        question = data.get("question")
        questionnaire_questions = Question.objects.filter(
            chapter__type=self.context.get("questionnairetype")
        )
        if question not in questionnaire_questions:
            raise ValidationError(
                {
                    "question_id": "Вопрос не соответствует анкете.",
                }
            )
        response = data.get("response")
        if question.answer_type == "choice_field":
            if response not in [
                option.text for option in question.question_parent.all()
            ]:
                raise ValidationError(
                    {
                        "question_id": question.id,
                        "response": f"Ответ должен быть выбран из "
                        f"вариантов ответов.",
                    }
                )
        return data

    def create(self, validated_data):
        """
        Создание ответа на вопрос.
        Если отправляется ответ на уже записанный в БД вопрос - ответ
        перезаписывается.
        При изменении ответа на вопрос, который имел субвопросы с ответами
        пользователя - ответы удаляются.
        """
        if QuestionResponse.objects.filter(
            order=self.context.get("order"),
            question=validated_data.get("question"),
        ).exists():
            instance = QuestionResponse.objects.get(
                order=self.context.get("order"),
                question=validated_data.get("question"),
            )

            instance.response = validated_data.get("response")
            instance.save()
            if instance.question.answer_type == "choice_field":
                questions = (
                    Question.objects.filter(option__question=instance.question)
                    .exclude(option__text=instance.response)
                    .all()
                )
                inner_questions = get_nested_questions(questions)
                all_inner_questions = inner_questions + [
                    question for question in questions
                ]
                QuestionResponse.objects.filter(
                    question__in=all_inner_questions
                ).delete()
        else:
            instance = QuestionResponse.objects.create(**validated_data)
        return instance


class OrderFullSerializer(serializers.ModelSerializer):
    """Сериализатор вывода всех ответов на анкету."""

    questionnaire_type_id = serializers.PrimaryKeyRelatedField(
        source="questionnaire_type", read_only=True
    )
    answers = QuestionResponseSerializer(
        source="questionresponse_set", many=True
    )

    class Meta:
        model = OrderModel
        fields = ["name", "questionnaire_type_id", "answers"]
