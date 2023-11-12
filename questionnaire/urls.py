from django.urls import path

from . import views


urlpatterns = [
<<<<<<< HEAD
=======
    path("category/<int:category_id>/questionnaires", views.get_questionnaire_types,
         name="questionnaire_types"),
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104
    path("questionnaire/<int:questionnaire_id>", views.get_questionnaire, name="get-get_questionnaire"),
]
