from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from app.orders.models import OrderModel, OrderFileData
from app.questionnaire.models import QuestionnaireCategory, QuestionnaireType, \
    Question, Option, QuestionnaireChapter, QuestionResponse


class OrderedByPositionSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('position')
        return super(OrderedByPositionSerializer, self).to_representation(data)


class QuestionnaireCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireCategory
        fields = ["id", "category"]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFileData
        fields = ["id", "original_name", "server_path", "yandex_path"]


class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = ["id", "question", "response"]


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
    options = OptionSerializer(read_only=True, many=True, source="question_parent")

    class Meta:
        model = Question
        list_serializer_class = OrderedByPositionSerializer
        fields = ["id", "text", "answer_type", "file_required", "answer_required", "options"]


    # def get_files(self, obj):
    #     key = self.context.get("key")
    #     if OrderModel.objects.filter(key=key,
    #                                  user_account__isnull=True).exists():
    #         order = OrderModel.objects.get(key=key, user_account__isnull=True)
    #         if OrderFileData.objects.filter(order_id=order, question_id=obj).exists():
    #             files = OrderFileData.objects.filter(order_id=order, question_id=obj).all()
    #             serializer = FileSerializer(files, many=True)
    #             return serializer.data
    #     return None
    #
    # def get_answer(self, obj):
    #     key = self.context.get("key")
    #     if OrderModel.objects.filter(key=key,
    #                                  user_account__isnull=True).exists():
    #         order = OrderModel.objects.get(key=key, user_account__isnull=True)
    #         if QuestionResponse.objects.filter(order=order, question=obj).exists():
    #             answer = QuestionResponse.objects.get(order=order, question=obj)
    #             serializer = QuestionResponseSerializer(answer)
    #             return serializer.data
    #     return None


class QuestionnaireChapterSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(read_only=True, many=True, source="question_set")

    class Meta:
        model = QuestionnaireChapter
        list_serializer_class = OrderedByPositionSerializer
        fields = ["id", "name", "questions"]


class QuestionnaireTypeSerializer(serializers.ModelSerializer):
    chapters = QuestionnaireChapterSerializer(read_only=True, many=True, source="questionnairechapter_set")

    class Meta:
        model = QuestionnaireType
        fields = ["id", "type", "description", "chapters"]


class QuestionnaireResponseSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(source="question", queryset=Question.objects.all())
    class Meta:
        model = QuestionResponse
        fields = ["id", "question_id", "response"]
        read_only_fields = ["id", "order"]

    def validate(self, data):
        question = data.get("question")
        questionnaire_questions = Question.objects.filter(chapter__type=self.context.get("questionnairetype"))
        if question not in questionnaire_questions:
            raise ValidationError({
                "question_id": "Вопрос не соответствует анкете.",
            })
        response = data.get("response")
        if question.answer_type == "choice_field":
            if response not in [option.text for option in question.question_parent.all()]:
                raise ValidationError({
                    "question_id": question.id,
                    "response": "Ответ должен быть выбран из вариантов ответов."
                })
        return data

    def create(self, validated_data):
        if QuestionResponse.objects.filter(order=self.context.get("order"),
                                           question=validated_data.get(
                                               "question")).exists():
            instance = QuestionResponse.objects.get(
                order=self.context.get("order"),
                question=validated_data.get("question"))

            instance.response = validated_data.get("response")
            instance.save()
            if instance.question.answer_type == "choice_field":
                questions = Question.objects.filter(option__question=instance.question).exclude(option__text=instance.response).all()
                inner_questions = get_nested_questions(questions)
                all_inner_questions = inner_questions + [question for question in questions]
                QuestionResponse.objects.filter(question__in=all_inner_questions).delete()
        else:
            instance = QuestionResponse.objects.create(**validated_data)
        return instance


def get_nested_questions(question_list):
    questions = []

    nested_questions = Question.objects.filter(
        option__question__in=question_list).all()
    questions += [question for question in nested_questions]
    if nested_questions:
        questions += get_nested_questions(nested_questions)
    return questions
