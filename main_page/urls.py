from django.conf import settings
from django.urls import include, path
from .views import FeedbackViewSet

from rest_framework import routers
router = routers.SimpleRouter()

router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    path('api/users/', include(router.urls)),
]
