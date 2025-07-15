from rest_framework import serializers

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

