from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


def send_verify_email(user):
    """
    Sends a verification email to the specified user.

    Generates a unique verification URL for the user and sends
    an email containing this URL to the user's registered email address.

    Args:
        user (User): The user object to whom the verification email will be sent.
    """

    token_generator = PasswordResetTokenGenerator()

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    domain = settings.DOMAIN
    verify_url = f'{domain}/accounts/verify-email/{uid}/{token}/'

    subject = 'Verify your email address'
    message = render_to_string(
        'emails/verify_email.html',
        {
            'user': user,
            'verify_url': verify_url,
        }
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=message
    )