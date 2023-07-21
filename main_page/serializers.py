from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer

from .models import UserAccount, CooperationOffer
from .validators import UserValidationFields

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "password", "person_telephone", "surname")


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("id", "email", "name", "person_telephone", "surname")
        validators = [UserValidationFields()]


class CooperationOfferSerializer(ModelSerializer):
    user_account_id = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = CooperationOffer
        fields = "__all__"


class TokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        print(self.user.email)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["test"] = "value"
        data["email"] = self.user.email


        return data

class CutomObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer
