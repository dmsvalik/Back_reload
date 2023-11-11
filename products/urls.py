from django.urls import path

from .views import CategoryAPIView


urlpatterns = [
    path("products/category/", CategoryAPIView.as_view()),
]
