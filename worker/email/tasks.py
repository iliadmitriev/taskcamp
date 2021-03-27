from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from worker.app import app


@app.task
def send_activation_email(email, url_link):
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
