import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(
    recipient: str,
    subject: str,
    body: str
):
    message = EmailMessage()

    message["From"] = EMAIL_USERNAME
    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(body)

    with smtplib.SMTP(
        EMAIL_HOST,
        EMAIL_PORT
    ) as server:
        server.starttls()
        server.login(
            EMAIL_USERNAME,
            EMAIL_PASSWORD
        )
        server.send_message(message)