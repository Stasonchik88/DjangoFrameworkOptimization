from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from authapp.models import ShopUser


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    subject = 'Подтвердите учетную запись'
    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
    send_mail(subject, message, 'noreply@localhost', [user.email])
