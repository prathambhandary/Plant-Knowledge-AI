import random
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def gen_random_number():
    return random.randint(1000, 9999)

def send_email(otp, TO_EMAIL):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    otp = str(otp)

    msg = MIMEText(otp)
    msg['Subject'] = f'Your OTP for Plant Knowledge AI'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        e
