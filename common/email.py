import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class Util:
    """
    Utility class for handling email-related operations.
    """


@staticmethod
def send_email(data):
    subject = data["subject"]
    to_email = data["to_email"]
    context = data["context"]

    html_message = render_to_string("reset_password_email.html", context)
    text_message = f"Click the link to reset your password: {context['reset_link']}"

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=os.getenv("EMAIL_FROM"),
        to=[to_email],
    )
    email.attach_alternative(html_message, "text/html")
    email.send()
