from products.models import Category
from questionnaire.models import QuestionnaireCategory, QuestionnaireType, QuestionnaireChapter, Question,\
    ANSWER_TYPES, Option
from .questionnaire_kitchen_full import main_information_chapter, main_facade_chapter


class QuestionnaireKitchenData(object):
    chapter_kitchen_full = ['Общая информация и разделы', 'Корпус и фасады', 'Фурнитура', 'Техника', 'Наполнение']
    all_chapters = [main_information_chapter, main_facade_chapter, ]

    def create_questionnaire_category(self):
        """ категорий анкет """
        all_categories = Category.objects.all()
        try:
            for item in all_categories:
                QuestionnaireCategory.objects.get_or_create(category=item)
        except Exception as e:
            print(e)

    def create_questionnaire_type(self):
        """ тип анкеты - короткая, полная """

        type_questionnaire = ['короткая', 'длинная']
        description_type_questionnaire = ['короткая анкета с минимальным количеством вопросов',
                                          'длинная анкета с полным описанием заказываемого товара и прикреплением файлов']

        all_questionnaire_category = QuestionnaireCategory.objects.all()
        try:
            for item in all_questionnaire_category:
                for x in range(len(type_questionnaire)):
                    QuestionnaireType.objects.get_or_create(
                        category=item,
                        type=type_questionnaire[x],
                        description=description_type_questionnaire[x],
                    )
        except Exception as e:
            print(e)

    def create_questionnaire_chapter(self):
        """ разделы внутри анкеты - пока только кухня (причем полная анкета) """

        category_kitchen = Category.objects.get(name='kitchen')
        full_questionnaire_type_kitchen = QuestionnaireType.objects.get(type='длинная', category=QuestionnaireCategory.objects.get(category=category_kitchen))

        try:
            for item in self.chapter_kitchen_full:
                QuestionnaireChapter.objects.get_or_create(
                    type=full_questionnaire_type_kitchen,
                    name=item,
                )
        except Exception as e:
            print(e)

    def create_questions_full_kitchen(self):

        try:
            for item_chapter in self.all_chapters:
                for item in item_chapter:
                    for key, value in item.items():

                        question = Question.objects.get_or_create(
                            text=key,
                            position=value['position'],
                            chapter=QuestionnaireChapter.objects.get(name=self.chapter_kitchen_full[0]),
                            answer_type=value['answer_type'],
                            file_required=value['file_required']
                        )

                        option_range = len(value['options'])
                        if option_range != 0:
                            for x in range(option_range):
                                dict_options = value['options'][x]
                                option = Option.objects.get_or_create(
                                    text=dict_options['text'],
                                    question=Question.objects.get(id=question[0].id),
                                    option_type=dict_options['option_type'],
                                )

                                question_range = len(dict_options['questions'])

                                if question_range != 0:
                                    for y in range(question_range):
                                        dict_questions = dict_options['questions'][y]
                                        print(dict_questions)
                                        Question.objects.get_or_create(
                                            text=dict_questions['text'],
                                            chapter=QuestionnaireChapter.objects.get(name=self.chapter_kitchen_full[0]),
                                            answer_type=dict_questions['answer_type'],
                                            file_required=dict_questions['file_required'],
                                            position=dict_questions['position'],
                                            option=Option.objects.get(id=option[0].id),
                                        )

        except Exception as e:
            print(f'error: {e}')
            pass






