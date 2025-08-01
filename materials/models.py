from django.db import models

from users.models import User


# Create your models here.


class Course(models.Model):
    """
    Модель обучающего курса.

    Attributes:
        name (str): Название курса.
        preview (Image): Картинка-превью (необязательно).
        description (str): Подробное описание содержания курса.
        owner (User): Владелец курса.
    """

    name = models.CharField(max_length=150, verbose_name="Название", help_text="Введите название курса")
    preview = models.ImageField(
        upload_to="course/preview", null=True, blank=True, verbose_name="Превью", help_text="Установите превью"
    )
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="courses", verbose_name="Владелец", null=True, blank=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Модель урока, входящего в курс.

    Attributes:
        name (str): Название урока.
        preview (Image): Картинка-превью (необязательно).
        description (str): Описание урока.
        link (str): URL-ссылка на видео.
        course (Course): Курс, к которому привязан урок.
        owner (User): Владелец урока.
    """

    name = models.CharField(max_length=150, verbose_name="Название", help_text="Введите название курса")
    preview = models.ImageField(
        upload_to="lesson/preview", null=True, blank=True, verbose_name="Превью", help_text="Установите превью"
    )
    description = models.TextField(verbose_name="Описание")
    link = models.URLField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name="Ссылка на видео",
        help_text="Ссылка на видео исключительно на youtube, проходит валидация",
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="lessons", verbose_name="Владелец", null=True, blank=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subs", verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="courses", verbose_name="Курс")
