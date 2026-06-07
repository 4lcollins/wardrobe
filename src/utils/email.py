import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.settings import SETTINGS

def send_email(subject, body, receiver_email):
    # Email details
    sender_email = SETTINGS.sender_email
    password = SETTINGS.icloud_sender_password

    # Build email
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "html"))

    # Send email
    with smtplib.SMTP("smtp.mail.me.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.send_message(message)
