from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer
from .models import ContactSupport, ContractorAgreement, CooperationOffer

User = get_user_model()


class CooperationOfferSerializer(ModelSerializer):
    """Сериализатор предложений о сотрудничестве."""

    class Meta:
        model = CooperationOffer
        fields = "__all__"


class ContactSupportSerializer(ModelSerializer):
    """Сериализатор вопросов относящихся к поддержке."""

    user_account = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = ContactSupport
        fields = [
            "id",
            "user_account",
            "user_question",
            "admin_response",
            "resolved",
        ]


class ContractorAgreementSerializer(serializers.ModelSerializer):
    """Сериализатор подтверждения договора о сотрудничестве."""

    class Meta:
        model = ContractorAgreement
        fields = ["user_account", "created_date"]
