from django.urls import path

from users import views
from users.apps import UsersConfig
from users.views import MyTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    # user
    path('user/<int:pk>/update/', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('user/create/', views.UserCreateAPIView.as_view(), name='user_create'),
    path('user/<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user'),

    # payment
    path('payments/', views.PaymentListAPIView.as_view(), name='payments'),
    path('payments/create/', views.PaymentCreateAPIView.as_view(), name='payments_create'),

    # token
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]