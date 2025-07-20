from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class User(AbstractUser):
    """
    Кастомная модель пользователя.

    Attributes:
        email (str): Адрес электронной почты.
        avatar (Image): Аватар пользователя.
        phone (int): Номер мобильного телефона.
        country (str): Название страны.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="E-mail", help_text="Введите адрес электронной почты")
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

    def __str__(self):
        return self.email


from materials.models import Course, Lesson


class Payment(models.Model):
    """
    Модель платежа пользователя

    Attributes:
        user (User): Ссылка на пользователя, который совершил платеж.
        date_of_pay (str): Дата платежа.
        paid_course (Course): Ссылка на оплаченный курс.
        paid_lesson (Lesson): Ссылка на оплаченный урок.
        payment_amount (int): Сумма платежа.
        payment_method (str): Способ оплаты (наличными/перевод на счет)
    """

    PAYMENT_METHOD_CHOICES = [("cash", "Наличными"), ("transfer", "Перевод на счет")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments", verbose_name="Пользователь")
    date_of_pay = models.DateTimeField(verbose_name="Дата оплаты", auto_now_add=True)
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="paid_courses",
        verbose_name="Оплаченные курсы",
        null=True,
        blank=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="paid_lessons",
        verbose_name="Оплаченные уроки",
        null=True,
        blank=True,
    )
    payment_amount = models.IntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=8, choices=PAYMENT_METHOD_CHOICES, default="cash", verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} - {self.date_of_pay} - {self.payment_amount}"
