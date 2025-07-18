from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['date_of_pay', ]


