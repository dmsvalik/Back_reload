from rest_framework import serializers

<<<<<<< HEAD
from questionnaire.models import QuestionnaireCategory, QuestionnaireType, Question, Option, QuestionnaireChapter
=======
from orders.models import OrderModel, OrderFileData
from questionnaire.models import QuestionnaireCategory, QuestionnaireType, \
    Question, Option, QuestionnaireChapter, QuestionResponse


class QuestionnaireShortTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireType
        fields = ["id", "type", "description"]
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104


class QuestionnaireCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireCategory
<<<<<<< HEAD
        fields = ["id", "name"]
=======
        fields = ["id", "category"]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFileData
        fields = ["id", "original_name", "server_path", "yandex_path"]


class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = ["id", "question", "response"]
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104


class OptionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ["id", "text", "option_type", "questions"]

    def get_questions(self, obj):
        queryset = Question.objects.filter(option=obj).order_by("position")
<<<<<<< HEAD
        serializer = QuestionSerializer(queryset, read_only=True, many=True)
=======
        serializer = QuestionSerializer(queryset, read_only=True, many=True,
                                        context={"key":self.context.get("key")})
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104
        return serializer.data


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
<<<<<<< HEAD

    class Meta:
        model = Question
        fields = ["id", "text", "answer_type", "file_required", "options"]

    def get_options(self, obj):
        queryset = Option.objects.filter(question=obj)
        serializer = OptionSerializer(queryset, read_only=True, many=True)
        return serializer.data

=======
    answer = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ["id", "text", "answer_type", "file_required", "answer", "files", "options"]

    def get_options(self, obj):
        queryset = Option.objects.filter(question=obj)
        serializer = OptionSerializer(queryset, read_only=True, many=True,
                                      context={"key": self.context.get("key")})
        return serializer.data

    def get_files(self, obj):
        key = self.context.get("key")
        if OrderModel.objects.filter(key=key,
                                     user_account__isnull=True).exists():
            order = OrderModel.objects.get(key=key, user_account__isnull=True)
            if OrderFileData.objects.filter(order_id=order, question_id=obj).exists():
                files = OrderFileData.objects.filter(order_id=order, question_id=obj).all()
                serializer = FileSerializer(files, many=True)
                return serializer.data
        return None

    def get_answer(self, obj):
        key = self.context.get("key")
        if OrderModel.objects.filter(key=key,
                                     user_account__isnull=True).exists():
            order = OrderModel.objects.get(key=key, user_account__isnull=True)
            if QuestionResponse.objects.filter(order=order, question=obj).exists():
                answer = QuestionResponse.objects.get(order=order, question=obj)
                serializer = QuestionResponseSerializer(answer)
                return serializer.data
        return None

>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104

class QuestionnaireChapterSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = QuestionnaireChapter
        fields = ["id", "name", "questions"]

    def get_questions(self, obj):
        queryset = Question.objects.filter(chapter=obj, option__isnull=True).order_by("position")
<<<<<<< HEAD
        serializer = QuestionSerializer(queryset, read_only=True, many=True)
=======
        serializer = QuestionSerializer(queryset, read_only=True, many=True,
                                        context={"key":self.context.get("key")})
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104
        return serializer.data


class QuestionnaireTypeSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField(read_only=True)
<<<<<<< HEAD

    class Meta:
        model = QuestionnaireType
        fields = ["id", "type", "description", "chapters"]

    def get_chapters(self, obj):
        queryset = QuestionnaireChapter.objects.filter(type=obj)
        serializer = QuestionnaireChapterSerializer(queryset, read_only=True, many=True)
        return serializer.data
=======
    answers_exists = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuestionnaireType
        fields = ["id", "type", "description", "answers_exists", "chapters"]

    def get_chapters(self, obj):
        queryset = QuestionnaireChapter.objects.filter(type=obj).order_by('position')
        serializer = QuestionnaireChapterSerializer(queryset, read_only=True, many=True,
                                                    context={"key":self.context.get("key")})
        return serializer.data

    def get_answers_exists(self, obj):
        key = self.context.get("key")
        if OrderModel.objects.filter(key=key, user_account__isnull=True).exists():
            order = OrderModel.objects.get(key=key, user_account__isnull=True)
            return QuestionResponse.objects.filter(order=order).exists()
        return False
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104
