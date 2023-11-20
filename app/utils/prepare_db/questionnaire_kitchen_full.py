
""" Общая информация и разделы """

main_information_chapter = [
    {
        'Какая по форме кухня':
            {'position': 1,
             'answer_type': 'choice_field',
             'file_required': False,
             'options': [{
                 "text": "Прямая",
                 "option_type": "answer",
                 "file_required": False,
                 "questions": []},
                 {
                     "text": "Угловая",
                     "option_type": "sub_questions",
                     "file_required": False,
                     "questions": [
                         {
                             "text": "Размер по стенам",
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
                     "file_required": False,
                     "questions": [
                         {
                             "text": "Размер по стенам",
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

        "Кухня до потолка":
            {
                'position': 2,
                "answer_type": "choice_field",
                "file_required": False,
                "options": [
                    {
                        "text": "Нет",
                        "option_type": "answer",
                        "file_required": False,
                        "questions": []
                    },
                    {
                        "text": "Да",
                        "option_type": "sub_questions",
                        "file_required": False,
                        "questions": [
                            {
                                "text": "Высота потолка",
                                'position': 1,
                                "answer_type": "text_field",
                                "file_required": False,
                                "options": []
                            },
                            {
                                "text": "Нужна ли фальш планка?",
                                'position': 2,
                                "answer_type": "text_field",
                                "file_required": False,
                                "options": []
                            }]
                    }],
            },

        "Глубина (ширина) столешницы?":
            {
                'position': 3,
                "answer_type": "text_field",
                "file_required": False,
                "options": []
            },

        "Нужен ли шкаф над холодильником для хранения?":
            {
                'position': 4,
                "answer_type": "text_field",
                "file_required": False,
                "options": []
            }

    }
]


""" Корпус и фасады """


main_facade_chapter = [
    {
        'В каких фасадах сделать расчет?':
            {'position': 1,
             'answer_type': 'choice_field',
             'file_required': False,
             'options': [{
                 "text": "Пленка",
                 "option_type": "answer",
                 "file_required": False,
                 "questions": []},
                 {
                     "text": "Эмаль",
                     "option_type": "sub_questions",
                     "file_required": False,
                     "questions": []},
                 {
                     "text": "Пластик",
                     "option_type": "sub_questions",
                     "file_required": False,
                     "questions": []},
                 {
                     "text": "ЛДСП",
                     "option_type": "answer",
                     "file_required": False,
                     "questions": []
                 }]
             },

        "Цвет фасадов?":
            {
                'position': 2,
                "answer_type": "text_field",
                "file_required": True,
                "options": [],
            },

        "Фасад с фрезеровкой/витраж/филенка. Приведите описание или приложите пример":
            {
                'position': 3,
                "answer_type": "text_field",
                "file_required": True,
                "options": []
            },

        "Цвет корпуса":
            {
                'position': 4,
                "answer_type": "text_field",
                "file_required": False,
                "options": []
            },

        'Столешница':
            {'position': 5,
             'answer_type': 'choice_field',
             'file_required': False,
             'options': [{
                 "text": "Пластик",
                 "option_type": "answer",
                 "file_required": False,
                 "questions": []},
                 {
                     "text": "Камень (мрамор/кварцит/гранит/оникс)",
                     "option_type": "sub_questions",
                     "file_required": False,
                     "questions": []},
                 {
                     "text": "Искуственный камень (акрил)",
                     "option_type": "sub_questions",
                     "file_required": False,
                     "questions": []},
                 {
                     "text": "Кварцевый агломерат",
                     "option_type": "answer",
                     "file_required": False,
                     "questions": []},
                 {
                     "text": "Компакт плита",
                     "option_type": "sub_questions",
                     "file_required": False,
                     "questions": []},
                 {
                     "text": "Керамогранит",
                     "option_type": "sub_questions",
                     "file_required": False,
                     "questions": []},
                 {
                     "text": "ЛДСП",
                     "option_type": "sub_questions",
                     "file_required": False,
                     "questions": []},

                 ]
             },

        'Необходим ли фартук?':
            {'position': 6,
             'answer_type': 'choice_field',
             'file_required': False,
             'options': [{
                 "text": "Нет",
                 "option_type": "answer",
                 "file_required": False,
                 "questions": []},
                 ]
             }

    }
]
