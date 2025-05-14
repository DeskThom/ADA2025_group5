import os
import smtplib
from email.mime.text import MIMEText
from flask import escape

FROM_EMAIL = 'aidencemails@gmail.com'
FROM_PASSWORD = 'xhspntpssdizvsnj'

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject    
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(FROM_EMAIL, FROM_PASSWORD)
        smtp.send_message(msg)

def send_email_to_user(request):
    try:
        request_json = request.get_json(silent=True)

        if not request_json or 'email' not in request_json:
            return "Missing 'email' in request body", 400

        email = request_json['email']
        send_email(email, "Welcome to our service!", "Thanks for creating an account.")
        return f"Email successfully sent to {escape(email)}", 200

    except Exception as e:
        return f"Error sending email: {escape(str(e))}", 500
