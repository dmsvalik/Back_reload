
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

