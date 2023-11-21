from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import ContactSupport, ContractorAgreement, CooperationOffer

User = get_user_model()


class CooperationOfferSerializer(ModelSerializer):

    class Meta:
        model = CooperationOffer
        fields = "__all__"


class ContactSupportSerializer(ModelSerializer):
    user_account = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = ContactSupport
        fields = [
            "id",
            "user_account",
            "user_question",
            "admin_response",
            "resolved"
        ]


class TokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["name"] = self.user.name
        data["email"] = self.user.email
        data["surname"] = self.user.surname

        return data


class CutomObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


class ContractorAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorAgreement
        fields = ['user_account', 'created_date']
