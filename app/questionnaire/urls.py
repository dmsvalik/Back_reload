from django.urls import path

from . import views


urlpatterns = [
    # path("category/<int:category_id>/questionnaires", views.get_questionnaire_types,
    #      name="questionnaire_types"),
    path(
        "questionnaire/<int:questionnaire_id>/",
        views.get_questionnaire,
        name="get-get_questionnaire",
    ),
    # path("questionnaire/<int:questionnaire_id>/answer", views.collect_answers, name="post-collect_answers"),
]
