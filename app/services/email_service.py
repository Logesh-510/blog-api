import smtplib
from email.message import EmailMessage

from ..settings import settings


def send_email(
    recipient_email: str,
    subject: str,
    body: str
):
    try:
        message = EmailMessage()

        message["From"] = settings.EMAIL_USERNAME
        message["To"] = recipient_email
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP(
            settings.EMAIL_HOST,
            settings.EMAIL_PORT
        ) as server:

            server.starttls()

            server.login(
                settings.EMAIL_USERNAME,
                settings.EMAIL_PASSWORD
            )

            server.send_message(message)

        print(f"Email sent successfully to {recipient_email}")

    except Exception as e:
        print(f"Email sending failed: {e}")
