from typing import Any

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}


class UserSerializer(serializers.ModelSerializer):
    history_of_payments = PaymentSerializer(many=True, read_only=True, source="payments")

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "avatar", "phone", "country", "history_of_payments"]


class PublicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "avatar", "country"]


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "password", "country"]
        extra_kwargs = {"password": {"write_only": True}}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email

        return token

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]: # После верного ввода логина и пароля, но до токена.
        data = super().validate(attrs)
        self.user.save() # Обновляется last_login, т.к. в модели auto_now=True
        return data
