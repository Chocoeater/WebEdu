from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User, Payment
from users.serializers import (
    UserSerializer,
    PaymentSerializer,
    MyTokenObtainPairSerializer,
    UserCreateSerializer,
    PublicUserSerializer,
)


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.id == obj.id or user.is_staff:
            return obj
        raise PermissionDenied("Доступ закрыт")


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    @swagger_auto_schema(operation_description="Возвращается полный профиль для админов и владельцев. Для остальных только публичные данные профиля.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        obj = self.get_object()
        user = self.request.user
        if user.id == obj.id or user.is_staff:
            return UserSerializer
        return PublicUserSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_description="Возвращается полный профиль для админов и владельцев. Для остальных только публичные данные профиля.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff:
            return UserSerializer
        return PublicUserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = [
        "date_of_pay",
    ]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]
