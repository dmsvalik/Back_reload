
from django.urls import include, path
from .views import CardModelAPIView


urlpatterns = [
    path('products/all_CardModel/', CardModelAPIView.as_view()),
]
