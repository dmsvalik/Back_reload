from app.questionnaire.models import (
    Question,
    QuestionnaireType,
    QuestionnaireChapter,
)


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


def collect_inner_questions(question: Question) -> list:
    """Получение вложенных вопросов, если они есть."""
    questions = []

    inner_questions = (
        Question.objects.filter(option__question=question)
        .order_by("position")
        .all()
    )
    if not inner_questions:
        return questions
    for inner_question in inner_questions:
        questions.append(inner_question)
        questions += collect_inner_questions(inner_question)
    return questions


def all_ordered_questions_in_questionnaire(
    questionnaire: QuestionnaireType,
) -> list:
    """Получение всех отсортированных вопросов в анкете."""
    questions = []
    chapters = (
        QuestionnaireChapter.objects.filter(type=questionnaire)
        .order_by("position")
        .all()
    )
    for chapter in chapters:
        outer_questions = Question.objects.filter(
            chapter=chapter, option__isnull=True
        )
        for question in outer_questions:
            questions.append(question)
            questions += collect_inner_questions(question)
    return questions
