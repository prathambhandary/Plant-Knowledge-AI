import random
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
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
    
    # HTML Content for the OTP landing page
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Plant Knowledge AI - OTP</title>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Special+Gothic+Condensed+One&display=swap">
    </head>
    <body style="background-color: #3aafa9; font-family: sans-serif; color: #feffff; text-align: center; padding: 50px;">
        <div style="background-color: #17252a; padding: 40px; border-radius: 25px; max-width: 500px; margin: 0 auto;">
            <h1 style="font-size: 36px; color: #feffff;">Welcome to <br>Plant Knowledge AI</h1>
            <p style="font-size: 24px; color: #feffff;">Your One-Time Password is:</p>
            <div style="font-size: 48px; font-weight: bold; background-color: #feffff; color: #17252a; padding: 10px 20px; border-radius: 10px; display: inline-block;">
                {otp}
            </div>
            <p style="font-size: 16px; color: #feffff; margin-top: 20px;">Use this OTP to verify your email. It will expire in a few minutes.</p>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['Subject'] = 'Your OTP for Plant Knowledge AI'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"OTP email sent to {TO_EMAIL}")
    except Exception as e:
        print(f"Error sending email: {e}")
