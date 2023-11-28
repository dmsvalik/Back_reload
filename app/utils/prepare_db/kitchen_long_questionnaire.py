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
                                 "question": "Размер по стенам. Если сможете сделать замер расположения вентканала, водопровода и   розеток – сделайте.",
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
                                 "question": "Размер по стенам. Если сможете сделать замер расположения вентканала, водопровода и   розеток – сделайте.",
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
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "Пластик",
                         "option_type": "answer",
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
                 "file_required": False,
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
                         "text": "Камень",
                         "option_type": "sub_questions",
                         "questions": [
                             {"question": 'Выберите тип камня',
                              'answer_type': 'choice_field',
                              'file_required': False,
                              'options': [
                                  {"text": "Мрамор",
                                   "option_type": "answer",
                                   "questions": []},
                                  {"text": "Кварцит",
                                   "option_type": "answer",
                                   "questions": []},
                                  {"text": "Гранит",
                                   "option_type": "answer",
                                   "questions": []},
                                  {"text": "Оникс",
                                   "option_type": "answer",
                                   "questions": []},
                              ]}, ]},
                     {
                         "text": "Искуственный камень (акрил)",
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "Кварцевый агломерат",
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "Компакт плита",
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "Керамогранит",
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "ЛДСП",
                         "option_type": "answer",
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
                     {"text": "Да",
                      "option_type": "sub_questions",
                      "questions": [
                          {"question": 'Выберите тип фартука',
                           'answer_type': 'choice_field',
                           'file_required': False,
                           'options': [
                               {
                                   "text": "Стеновая панель",
                                   "option_type": "answer",
                                   "questions": []},
                               {
                                   "text": "Покраска",
                                   "option_type": "answer",
                                   "questions": []},
                               {
                                   "text": "Стекло",
                                   "option_type": "answer",
                                   "questions": []},
                           ]},
                      ]
                      },
                 ]
                 },
                {"question": 'Необходим ли плинтус?',
                 'position': 7,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []}
            ]
        },
        {
            "name": "Фурнитура",
            "questions": [
                {"question": 'В какой фурнитуре сделать расчет?',
                 'position': 1,
                 'answer_type': 'choice_field',
                 'file_required': False,
                 'options': [
                     {
                         "text": "Простой сегмент",
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "Cредний сегмент",
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "Топ сегмент",
                         "option_type": "answer",
                         "questions": []},
                 ]},
                {"question": 'Если нужна конкретная фирма, пожалуйста расскажите нам',
                 'position': 2,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Необходим ли цоколь?',
                 'position': 3,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Какие ручки?',
                 'position': 4,
                 'answer_type': 'choice_field',
                 'file_required': False,
                 'options': [
                     {
                         "text": "Ручка-кнопка",
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "Открывание от нажатия",
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "Открывание за фасад",
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "Интегрированная ручка",
                         "option_type": "answer",
                         "questions": []},
                     {
                         "text": "Ручка-скоба",
                         "option_type": "answer",
                         "questions": []},
                 ]},
                {"question": 'Цвет ручек?',
                 'position': 5,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Нужны ли подъемные механизмы?',
                 'position': 6,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {
                    "question": 'Нужны ли фальш планки с боков гарнитура? (с фальш планками легче скрывать неровности стен).',
                    'position': 7,
                    'answer_type': 'text_field',
                    'file_required': False,
                    'options': []},
            ]},
        {
            "name": "Техника",
            "questions": [
                {"question": 'Предусмотреть ли выдвижные розетки?',
                 'position': 1,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Вытяжка (уточните модель)',
                 'position': 2,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Духовой шкаф модель',
                 'position': 3,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Посудомойка будет?',
                 'position': 4,
                 'answer_type': 'choice_field',
                 'file_required': False,
                 'options': [{
                     "text": "Нет",
                     "option_type": "answer",
                     "questions": []},
                     {"text": "Да",
                      "option_type": "sub_questions",
                      "questions": [
                          {"question": 'Ширина посудомойки',
                           'answer_type': 'choice_field',
                           'file_required': False,
                           'options': [
                               {
                                   "text": "450 мм",
                                   "option_type": "answer",
                                   "questions": []},
                               {
                                   "text": "600 мм",
                                   "option_type": "answer",
                                   "questions": []},
                           ]},
                          {"question": 'Уточните модель',
                           'answer_type': 'text_field',
                           'file_required': False,
                           'options': []}
                      ]
                      }
                 ]},
                {"question": 'Варочная отдельно стоящая или встраиваемая, на 2 или 4 конфорки? (уточните модель)',
                 'position': 5,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Холодильник встроенный или отдельно стоящий? ',
                 'position': 6,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Микроволновая печь, встроенная или отдельно стоящая? (уточните модель)',
                 'position': 7,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
            ]},
        {
            "name": "Наполнение",
            "questions": [
                {"question": 'Предусмотрена ли бутылочница?',
                 'position': 1,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Посудосушитель верхний/нижний',
                 'position': 2,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Предусмотреть двойной выдвижной ящик с ящиком для приборов?',
                 'position': 3,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Если уже определились с раковиной, уточните модель',
                 'position': 4,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
                {"question": 'Нужна ли подсветка?',
                 'position': 5,
                 'answer_type': 'choice_field',
                 'file_required': False,
                 'options': [{
                     "text": "Нет",
                     "option_type": "answer",
                     "questions": []},
                     {"text": "Да",
                      "option_type": "sub_questions",
                      "questions": [
                          {"question": 'Опишите расположение',
                           'answer_type': 'text_field',
                           'file_required': False,
                           'options': []},
                          {"question": 'Цвет',
                           'answer_type': 'text_field',
                           'file_required': False,
                           'options': []},
                          {"question": 'Нужна ли подсветка профиль-ручки',
                           'answer_type': 'text_field',
                           'file_required': False,
                           'options': []},
                           ]},
                     ]}
            ]},
        {
            "name": "Дополнительная информация",
            "questions": [
                {"question": 'Опишите дополнительную информацию своими словами.',
                 'position': 1,
                 'answer_type': 'text_field',
                 'file_required': False,
                 'options': []},
            ]}

    ]}
