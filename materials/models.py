from django.db import models

# Create your models here.

class Course(models.Model):
    """
    Модель обучающего курса.

    Attributes:
        name (str): Название курса.
        preview (Image): Картинка-превью (необязательно).
        description (str): Подробное описание содержания курса.
    """

    name = models.CharField(max_length=150, verbose_name='Название', help_text='Введите название курса')
    preview = models.ImageField(upload_to='course/preview', null=True, blank=True, verbose_name='Превью', help_text='Установите превью')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

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
    """

    name = models.CharField(max_length=150, verbose_name='Название', help_text='Введите название курса')
    preview = models.ImageField(upload_to='lesson/preview', null=True, blank=True, verbose_name='Превью', help_text='Установите превью')
    description = models.TextField(verbose_name='Описание')
    link = models.URLField(max_length=300, null=True, blank=True, verbose_name='Ссылка на видео', help_text='Вставьте ссылку на видео-урок')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name