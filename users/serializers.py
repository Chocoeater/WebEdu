from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, Payment

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    history_of_payments = PaymentSerializer(many=True, read_only=True, source='payments')

    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'country', 'history_of_payments']


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token