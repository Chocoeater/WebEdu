from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="E-mail", help_text="Введите адрес электронной почты"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        null=True,
        blank=True,
        verbose_name="Аватар",
        help_text="Загрузите изображение для аватара",
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name="Номер мобильного телефона",
        help_text="Введите ваш номер мобильного телефона",
    )
    country = models.CharField(
        max_length=40,
        verbose_name="Страна",
        help_text="Введите название страны, в которой вы находитесь",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        permissions = [
            ("can_block_user", "Может заблокировать пользователя"),
        ]

    def __str__(self):
        return self.email
