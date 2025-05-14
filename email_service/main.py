import smtplib
from email.mime.text import MIMEText
import functions_framework
from flask import Flask, request

FROM_EMAIL = 'aidencemails@gmail.com'
FROM_PASSWORD = 'xhspntpssdizvsnj'


def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject    
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(FROM_EMAIL, FROM_PASSWORD)
        response = smtp.send_message(msg)
        if response == {}:
            return True
        return False

@functions_framework.http
def send_email_to_user(request):

    request_json = request.get_json(silent=True)

    if not request_json or 'email' not in request_json:
        return "Missing 'email' in request body", 400

    email = request_json['email']
    if send_email(email, "Welcome to our service!", "Thanks for creating an account."):
        return f"Email successfully sent to {email}", 200
    return f"Failed to send email to {email}", 500
