from django.urls import include, path
from .views import CardModelAPIView, CategoryModelListAPIView


urlpatterns = [
    path('products/all_CardModel/', CardModelAPIView.as_view()),
    path('products/card_categories/<int:card_id>', CategoryModelListAPIView.as_view())
]
