questionnaire = {
    "Category": "Кухня",
    "Type": "Полная",
    "Chapters": [
        {
            "name": "Общая информация и размеры",
            "questions": [
                {"question": 'Какая по форме кухня',
                 'position': 1,
                 'answer_type': 'choice_field',
                 'file_required': False,
                 'options': [{
                                 "text": "Прямая",
                                 "option_type": "answer",
                                 "questions": []},
                             {
                                 "text": "Угловая",
                                 "option_type": "sub_questions",
                                 "questions": [
                                     {
                                         "question": "Размер по стенам",
                                         'position': 1,
                                         "answer_type": "text_field",
                                         "file_required": False,
                                         "options": []
                                     }
                                 ]
                             },
                             {
                                 "text": "\"П\"-образная",
                                 "option_type": "sub_questions",
                                 "questions": [
                                     {
                                         "question": "Размер по стенам",
                                         'position': 1,
                                         "answer_type": "text_field",
                                         "file_required": False,
                                         "options": []
                                     }
                                 ]
                             },
                             {
                                 "text": "Островная",
                                 "option_type": "answer",
                                 "file_required": False,
                                 "questions": []
                             },
                             {
                                 "text": "Параллельная",
                                 "option_type": "answer",
                                 "file_required": False,
                                 "questions": []
                             }]
                 },

                {"question": "Кухня до потолка",
                 'position': 2,
                 "answer_type": "choice_field",
                 "file_required": False,
                 "options": [
                                {
                                    "text": "Нет",
                                    "option_type": "answer",
                                    "questions": []
                                },
                                {
                                    "text": "Да",
                                    "option_type": "sub_questions",
                                    "questions": [
                                        {
                                            "question": "Высота потолка",
                                            'position': 1,
                                            "answer_type": "text_field",
                                            "file_required": False,
                                            "options": []
                                        },
                                        {
                                            "question": "Нужна ли фальш планка?",
                                            'position': 2,
                                            "answer_type": "text_field",
                                            "file_required": False,
                                            "options": []
                                        }]
                                }],
                 },

                {"question": "Глубина (ширина) столешницы?",
                 'position': 3,
                 "answer_type": "text_field",
                 "file_required": False,
                 "options": []
                 },

                {"question": "Нужен ли шкаф над холодильником для хранения?",
                 'position': 4,
                 "answer_type": "text_field",
                 "file_required": False,
                 "options": []
                 }
            ]
        },
        {
            "name": "Корпус и фасады",
            "questions": [
                {"question": 'В каких фасадах сделать расчет?',
                 'position': 1,
                 'answer_type': 'choice_field',
                 'file_required': False,
                 'options': [{
                             "text": "Пленка",
                             "option_type": "answer",
                             "questions": []},
                             {
                                 "text": "Эмаль",
                                 "option_type": "sub_questions",
                                 "questions": []},
                             {
                                 "text": "Пластик",
                                 "option_type": "sub_questions",
                                 "questions": []},
                             {
                                 "text": "ЛДСП",
                                 "option_type": "answer",
                                 "questions": []
                             }]
                         },

                {"question": "Цвет фасадов?",
                 'position': 2,
                 "answer_type": "text_field",
                 "file_required": True,
                 "options": [],
                 },

                {"question": "Фасад с фрезеровкой/витраж/филенка. Приведите описание или приложите пример",
                 'position': 3,
                 "answer_type": "text_field",
                 "file_required": True,
                 "options": []
                 },

                {"question": "Цвет корпуса",
                 'position': 4,
                 "answer_type": "text_field",
                 "file_required": False,
                 "options": []
                 },

                {"question": 'Столешница',
                 'position': 5,
                 'answer_type': 'choice_field',
                 'file_required': False,
                 'options': [{
                             "text": "Пластик",
                             "option_type": "answer",
                             "questions": []},
                             {
                                 "text": "Камень (мрамор/кварцит/гранит/оникс)",
                                 "option_type": "sub_questions",
                                 "questions": []},
                             {
                                 "text": "Искуственный камень (акрил)",
                                 "option_type": "sub_questions",
                                 "questions": []},
                             {
                                 "text": "Кварцевый агломерат",
                                 "option_type": "answer",
                                 "questions": []},
                             {
                                 "text": "Компакт плита",
                                 "option_type": "sub_questions",
                                 "questions": []},
                             {
                                 "text": "Керамогранит",
                                 "option_type": "sub_questions",
                                 "questions": []},
                             {
                                 "text": "ЛДСП",
                                 "option_type": "sub_questions",
                                 "questions": []},

                             ]
                 },

                {"question": 'Необходим ли фартук?',
                 'position': 6,
                 'answer_type': 'choice_field',
                 'file_required': False,
                 'options': [{
                             "text": "Нет",
                             "option_type": "answer",
                             "questions": []},
                             ]
                         },

            ]
        }
    ]
}
