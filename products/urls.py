from django.urls import path

from .views import (AnswerListAPIView, CardModelAPIView, ImageResponseAPIView,
                    CategoryModelListAPIView, QuestionsModelListAPIView, CreateOrderAnswers)


urlpatterns = [
    path("products/step_1/card/", CardModelAPIView.as_view()),
    path("products/step_2/<int:card_id>", CategoryModelListAPIView.as_view()),
    path(
        "products/step_3_1/<int:category_id>/questions",
        QuestionsModelListAPIView.as_view(),
    ),
    path("products/step_3_2/questions_response", AnswerListAPIView.as_view()),
    path("products/step_4/create_order", CreateOrderAnswers),
    path("products/responses/image", ImageResponseAPIView.as_view())
]
