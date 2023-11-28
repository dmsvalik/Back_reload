from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet

category_router = routers.DefaultRouter()
category_router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(category_router.urls), name="category"),
]
