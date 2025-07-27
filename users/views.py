
from django_filters.rest_framework import DjangoFilterBackend

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
from users.services import convert_rub_to_usd, create_stripe_price, create_stripe_session, create_stripe_product


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

    @swagger_auto_schema(
        operation_description="Возвращается полный профиль для админов и владельцев. "
                              "Для остальных только публичные данные профиля."
    )
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
        operation_description="Возвращается полный профиль для админов и владельцев. "
                              "Для остальных только публичные данные профиля."
    )
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

    def perform_create(self, serializer):

        payment = serializer.save(user=self.request.user)

        if payment.paid_course:
            product_name = f"Курс: {payment.paid_course.name}"
        elif payment.paid_lesson:
            product_name = f"Урок: {payment.paid_lesson.name}"
        else:
            product_name = "Платеж"

        amount_in_dollar = convert_rub_to_usd(payment.payment_amount)

        product = create_stripe_product(product_name)
        price = create_stripe_price(amount_in_dollar, product.id)

        session_id, payment_link = create_stripe_session(price.id)

        payment.session_id = session_id
        payment.link_for_pay = payment_link
        payment.save()


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
