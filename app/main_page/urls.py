from django.urls import include, path
from rest_framework import routers

from .views import ContractorAgreementViewSet, CooperationViewSet, SupportViewSet


router = routers.SimpleRouter()
router.register(r"support", SupportViewSet)

urlpatterns = [
    path("contact/cooperation/", CooperationViewSet.as_view({"post": "create"})),
    path("contact/", include(router.urls)),
    path("contractor_agreement", ContractorAgreementViewSet.as_view({"post": "create"})),
]
