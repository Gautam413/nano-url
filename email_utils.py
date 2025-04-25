import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
# from models import VerificationToken
import os
import random
import string
from datetime import datetime, timezone, timedelta

import jwt 
SECRET_KEY = os.getenv("JWT_SEC")  # For JWT

# Generate a unique verification token
def generate_token(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to send email

def send_email(to_email: str, subject: str, body: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    email_user = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = to_email

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_user, email_password)
        server.sendmail(email_user, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")





def generate_verification_token(email: str, short_url: str):
    payload = {
        "user_email": email,
        "short_url": short_url,
        "exp": int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp())  # 1-day expiration
    }
    print(f"SECRET_KEY: {SECRET_KEY}, type: {type(SECRET_KEY)}")

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token if isinstance(token, str) else token.decode("utf-8")
    # return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


# ✅ Send Verification Email with JWT
def send_verification_email(to_email: str, short_url: str, base_url: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    email_user = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")

     # ✅ Debugging: Check types before using
    print(f"to_email: {to_email}, type: {type(to_email)}")
    print(f"email_user: {email_user}, type: {type(email_user)}")

    print(f"repr(email_user): {repr(email_user)}")
    print(f"repr(to_email): {repr(to_email)}")


    if not all([smtp_server, smtp_port, email_user, email_password]):
        raise ValueError("Missing one or more required email environment variables.")

    try:
        print("About to generate token...")
        token = generate_verification_token(to_email, short_url)
        print(f"Generated token: {token}, type: {type(token)}")
    except Exception as e:
        print(f"Error generating token: {e}")
        raise

    # token = generate_verification_token(to_email, short_url)  # ✅ Generate JWT token


    # verification_link = f"http://127.0.0.1:8000/verify/{token}"  # ✅ Use token in URL
    # verification_link = f"{base_url}verify/{token}"
    verification_link = f"{base_url.rstrip('/')}/verify/{token}"

    subject = "Verify Your Access"
    body = f"Click <a href='{verification_link}'>here</a> to verify your access. This link will expire in 24 hours."

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = to_email
    
    print(f"msg headers -> From: {email_user}, To: {to_email}")


    try:
        print(f"Sending email from {email_user} to {to_email}")
        print(f"msg.as_string():\n{msg.as_string()}")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_user, email_password)

        server.sendmail(email_user, to_email, msg.as_string())
        server.quit()
        print("Verification email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def notify_creator(creator_email: str, user_email: str, original_url: str):
    subject = "Your Short URL Has Been Accessed"
    body = f"User {user_email} has accessed your short URL. <br>Original URL: {original_url}"

    send_email(creator_email, subject, body)
