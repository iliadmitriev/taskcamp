from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import loader
from worker.app import app


@app.task(
    max_retries=5,
    default_retry_delay=60,
    autoretry_for=(ConnectionRefusedError,)
    )
def send_activation_email(email, url_link):
    subject = 'Your taskcamp account activation'

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


@app.task
def send_welcome_message(email, tour_link):
    subject = 'Taskcamp welcomes you'

    html_message = render_to_string(
        'email/register_welcome.html',
        {'tour_link': tour_link}
    )

    txt_message = render_to_string(
        'email/register_welcome.txt',
        {'tour_link': tour_link}
    )

    message = EmailMultiAlternatives(
        subject,
        txt_message,
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )

    message.attach_alternative(html_message, 'text/html')

    return message.send()


@app.task(
    max_retries=5,
    default_retry_delay=60,
    autoretry_for=(ConnectionRefusedError,)
    )
def send_reset_email(
        subject_template_name, email_template_name,
        context, from_email, to_email, html_email_template_name=None):
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()
