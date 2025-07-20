from django.urls import path

from users import views
from users.apps import UsersConfig
from users.views import MyTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    # user
    path("<int:pk>/update/", views.UserUpdateAPIView.as_view(), name="user_update"),
    path("create/", views.UserCreateAPIView.as_view(), name="user_create"),
    path("<int:pk>/", views.UserRetrieveAPIView.as_view(), name="user"),
    path("", views.UserListAPIView.as_view(), name="users"),
    path("<int:pk>/delete", views.UserListAPIView.as_view(), name="user_delete"),
    # payment
    path("payments/", views.PaymentListAPIView.as_view(), name="payments"),
    path("payments/create/", views.PaymentCreateAPIView.as_view(), name="payments_create"),
    # token
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
]
