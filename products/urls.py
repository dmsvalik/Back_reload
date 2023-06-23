from django.urls import path

from .views import (AnswerListAPIView, CardModelAPIView,
                    CategoryModelListAPIView, QuestionsModelListAPIView)


urlpatterns = [
    path("products/all_CardModel/", CardModelAPIView.as_view()),
    path("products/card_categories/<int:card_id>", CategoryModelListAPIView.as_view()),
    path(
        "products/category/<int:category_id>/questions",
        QuestionsModelListAPIView.as_view(),
    ),
    path("products/questions_response", AnswerListAPIView.as_view()),

    # path('products/image', ProductImageViewSet.as_view()),
]
