from django.urls import path

from . import views


urlpatterns = [
    path("questionnaire/<int:questionnaire_id>", views.get_questionnaire, name="get-get_questionnaire"),
]
