import os
import smtplib
from email.mime.text import MIMEText
from flask import escape

FROM_EMAIL = 'aidencemails@gmail.com'
FROM_PASSWORD = 'xhspntpssdizvsnj'
message = '''
Hi [User’s First Name],

Welcome to Aidence – where we’re all about scanning the future, one CT scan at a time! 🚀

You’re now all set to take a deep breath and let us do the heavy lifting. Our AI is ready to analyze your lung CT scans and provide you with accurate, timely insights – no guesswork, just data-backed clarity.

Here’s what you can expect:
✅ Fast and reliable scan analysis.
✅ Early detection of potential issues.
✅ Easy-to-understand reports.

Ready to get started? Log in here: [Login Link]

We’re here to help you breathe easier. Got questions? Reach out to our support team anytime. We’re all ears (and lungs!).

Stay healthy,
The Aidence Team

P.S. Remember – when it comes to your lungs, we’ve got you covered, right down to the last pixel! 🖥️✨
'''

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
        send_email(email, "Welcome to our service!", message)
        return f"Email successfully sent to {escape(email)}", 200

    except Exception as e:
        return f"Error sending email: {escape(str(e))}", 500
