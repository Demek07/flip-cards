from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse


def send_activation_email(request, user, token):
    """
    Отправляет email с ссылкой для активации аккаунта
    """
    activation_url = request.build_absolute_uri(
        reverse('users:activate_account') + f'?token={token}'
    )

    print(activation_url)

    context = {
        'user': user,
        'activation_url': activation_url,
        'valid_days': getattr(settings, 'EMAIL_ACTIVATION_TIMEOUT_DAYS', 7)
    }

    # Рендерим HTML и текстовую версию письма
    html_message = render_to_string('users/activation_email.html', context)
    plain_message = strip_tags(html_message)

    # Отправляем письмо
    send_mail(
        subject='Активация аккаунта на сайте Flip-Cards',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
