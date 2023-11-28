from app.products.models import Category
from app.questionnaire.models import QuestionnaireCategory, QuestionnaireType, QuestionnaireChapter, Question, \
    Option
from .questionnaire_kitchen_full import main_information_chapter, main_facade_chapter


class QuestionnaireKitchenData(object):
    # chapter_kitchen_full = ['Общая информация и разделы', 'Корпус и фасады', 'Фурнитура', 'Техника', 'Наполнение']
    # all_chapters = [main_information_chapter, main_facade_chapter, ]
    #
    # def create_questionnaire_category(self):
    #     """ категорий анкет """
    #     all_categories = Category.objects.all()
    #     try:
    #         for item in all_categories:
    #             QuestionnaireCategory.objects.get_or_create(category=item)
    #     except Exception as e:
    #         print(e)
    #
    # def create_questionnaire_type(self):
    #     """ тип анкеты - короткая, полная """
    #
    #     type_questionnaire = ['короткая', 'длинная']
    #     description_type_questionnaire = ['короткая анкета с минимальным количеством вопросов',
    #                                       'длинная анкета с полным описанием заказываемого товара и прикреплением файлов']
    #
    #     all_questionnaire_category = QuestionnaireCategory.objects.all()
    #     try:
    #         for item in all_questionnaire_category:
    #             for x in range(len(type_questionnaire)):
    #                 QuestionnaireType.objects.get_or_create(
    #                     category=item,
    #                     type=type_questionnaire[x],
    #                     description=description_type_questionnaire[x],
    #                 )
    #     except Exception as e:
    #         print(e)
    #
    # def create_questionnaire_chapter(self):
    #     """ разделы внутри анкеты - пока только кухня (причем полная анкета) """
    #
    #     category_kitchen = Category.objects.get(name='kitchen')
    #     full_questionnaire_type_kitchen = QuestionnaireType.objects.get(type='длинная', category=QuestionnaireCategory.objects.get(category=category_kitchen))
    #
    #     try:
    #         for item in self.chapter_kitchen_full:
    #             QuestionnaireChapter.objects.get_or_create(
    #                 type=full_questionnaire_type_kitchen,
    #                 name=item,
    #             )
    #     except Exception as e:
    #         print(e)
    #
    # def create_questions_full_kitchen(self):
    #
    #     try:
    #         for item_chapter in self.all_chapters:
    #             for item in item_chapter:
    #                 for key, value in item.items():
    #
    #                     question = Question.objects.get_or_create(
    #                         text=key,
    #                         position=value['position'],
    #                         chapter=QuestionnaireChapter.objects.get(name=self.chapter_kitchen_full[0]),
    #                         answer_type=value['answer_type'],
    #                         file_required=value['file_required']
    #                     )
    #
    #                     option_range = len(value['options'])
    #                     if option_range != 0:
    #                         for x in range(option_range):
    #                             dict_options = value['options'][x]
    #                             option = Option.objects.get_or_create(
    #                                 text=dict_options['text'],
    #                                 question=Question.objects.get(id=question[0].id),
    #                                 option_type=dict_options['option_type'],
    #                             )
    #
    #                             question_range = len(dict_options['questions'])
    #
    #                             if question_range != 0:
    #                                 for y in range(question_range):
    #                                     dict_questions = dict_options['questions'][y]
    #                                     print(dict_questions)
    #                                     Question.objects.get_or_create(
    #                                         text=dict_questions['text'],
    #                                         chapter=QuestionnaireChapter.objects.get(name=self.chapter_kitchen_full[0]),
    #                                         answer_type=dict_questions['answer_type'],
    #                                         file_required=dict_questions['file_required'],
    #                                         position=dict_questions['position'],
    #                                         option=Option.objects.get(id=option[0].id),
    #                                     )
    #
    #     except Exception as e:
    #         print(f'error: {e}')
    #         pass

    def create_chapter(self, chapter_data, type):
        chapter, _ = QuestionnaireChapter.objects.get_or_create(
            name=chapter_data["name"],
            type=type
        )
        for question_data in chapter_data["questions"]:
            self.create_question(question_data, chapter)

    def create_question(self, question_data, chapter, option=None):
        question, _ = Question.objects.get_or_create(
            text=question_data["question"],
            position=question_data["position"] if "position" in question_data else None,
            chapter=chapter,
            answer_type=question_data["answer_type"],
            file_required=question_data["file_required"],
            option=option
        )
        if question_data["options"]:
            for option_data in question_data["options"]:
                self.create_option(option_data, question, chapter)

    def create_option(self, option_data, question, chapter):
        option, _ = Option.objects.get_or_create(
            text=option_data["text"],
            question=question,
            option_type=option_data["option_type"]
        )
        if option_data["questions"]:
            for question_data in option_data["questions"]:
                self.create_question(question_data, chapter, option)

    def create_data(self, questionnaire):
        try:
            category, _ = Category.objects.get_or_create(name=questionnaire["Category"])
            questionnaire_type, _ = QuestionnaireType.objects.get_or_create(
                category=category,
                type=questionnaire["Type"],
                description=None
            )
            for chapter_data in questionnaire["Chapters"]:
                self.create_chapter(chapter_data, questionnaire_type)
        except Exception as er:
            print(f'error: {er}')
            pass
