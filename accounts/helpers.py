import uuid

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def generate_user_hash_and_token(user_id):
    user_hash = uuid.uuid4().hex
    token = uuid.uuid4().hex

    cache.set(
        user_hash,
        {
            'token': token,
            'user_id': user_id
        },
        settings.ACCOUNT_ACTIVATION_LINK_EXPIRE
    )
    return user_hash, token


def send_register_activation_email(email, url_link):
    subject = 'Your account activation'

    html_message = render_to_string(
        'email/register_activate.html',
        {'url_link': url_link}
    )

    txt_message = render_to_string(
        'email/register_activate.txt',
        {'url_link': url_link}
    )

    message = EmailMultiAlternatives(
        subject,
        txt_message,
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )

    message.attach_alternative(html_message, 'text/html')

    return message.send()