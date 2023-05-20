from django.urls import include, path
from .views import *

urlpatterns = [
    path('products/image', OrderImageViewSet.as_view()),
]
