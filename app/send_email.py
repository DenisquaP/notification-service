import os
from dotenv import load_dotenv

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL = os.getenv("EMAIL")
SMTP_NAME = os.getenv("SMTP_NAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(
    to_email: str = "",
    message: str = ""
):
    smtp_server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    smtp_server.login(EMAIL, SMTP_PASSWORD)

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = SMTP_NAME

    text = message
    msg.attach(MIMEText(text, "plain"))

    smtp_server.sendmail(EMAIL, to_email, msg.as_string())
    smtp_server.quit()
