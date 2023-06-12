from django.conf import settings
from django.urls import include, path
from .views import ActivateUser, reset_password
from .views import CooperationViewSet, ActivateUser, reset_password

from rest_framework import routers
router = routers.SimpleRouter()

router.register(r'cooperation', CooperationViewSet)

urlpatterns = [
    path('users/', include(router.urls)),
    path('activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path('password/reset/confirm/<str:uid>/<str:token>', reset_password, name='reset_password'),
]
