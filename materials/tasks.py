from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from pyexpat.errors import messages


@shared_task
def send_about_sub(message, user):
    send_mail(
        subject='Информация об изменении статуса подписки',
        message=message, # Для теста не буду усложнять
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )