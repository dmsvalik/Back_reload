from products.models import Category
from questionnaire.models import QuestionnaireCategory, QuestionnaireType, QuestionnaireChapter, Question


class QuestionnaireData(object):

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

        chapter_kitchen_full = ['Общая информация и разделы', 'Корпус и фасады', 'Фурнитура', 'Техника', 'Наполнение']
        category_kitchen = Category.objects.get(name='kitchen')
        full_questionnaire_type_kitchen = QuestionnaireType.objects.get(type='длинная', category=QuestionnaireCategory.objects.get(category=category_kitchen))

        try:
            for item in chapter_kitchen_full:
                QuestionnaireChapter.objects.get_or_create(
                    type=full_questionnaire_type_kitchen,
                    name=item,
                )
        except Exception as e:
            print(e)


    def create_questions_full_kitchen(self):

        pass
        # questions = [
        #
        # ]
        # try:
        #     for item in chapter_kitchen_full:
        #         Question.objects.get_or_create(
        #             chapter=QuestionnaireChapter.objects.get(name=item)
        #         )
        # except Exception as e:
        #     print(e)






