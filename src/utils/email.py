import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.settings import SETTINGS


def send_email(subject, body, receiver_email=None, bcc_emails=None):
    bcc_emails = bcc_emails or []
    recipients = [email for email in [receiver_email, *bcc_emails] if email]
    if not recipients:
        raise ValueError("At least one recipient email is required.")

    # Email details
    sender_email = SETTINGS.sender_email
    password = SETTINGS.gmail_app_password

    # Build email
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email or sender_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "html"))

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.send_message(message, to_addrs=recipients)
