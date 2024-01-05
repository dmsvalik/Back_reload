from app.questionnaire.models import Question


def get_nested_questions(question_list: list) -> list:
    """Получение все вложенных вопросов, если они есть."""
    questions = []

    nested_questions = Question.objects.filter(
        option__question__in=question_list
    ).all()
    questions += [question for question in nested_questions]
    if nested_questions:
        questions += get_nested_questions(nested_questions)
    return questions
