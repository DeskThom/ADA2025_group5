import smtplib
from email.mime.text import MIMEText
import functions_framework
from flask import Flask, request

FROM_EMAIL = 'aidencemails@gmail.com'
FROM_PASSWORD = 'xhspntpssdizvsnj'
message1 = '''
Hi Indika,

Welcome to Aidence – where we’re all about scanning the future, one CT scan at a time! 

You’re now all set to take a deep breath and let us do the heavy lifting. Our AI is ready to analyze your lung CT scans and provide you with accurate, timely insights – no guesswork, just data-backed clarity.

Here’s what you can expect:
Fast and reliable scan analysis.
Early detection of potential issues.
Easy-to-understand reports.

Ready to get started? Log in here: [Login Link]

We’re here to help you breathe easier. Got questions? Reach out to our support team anytime. We’re all ears (and lungs!).

Stay healthy,
The Aidence Team

P.S. Remember – when it comes to your lungs, we’ve got you covered, right down to the last pixel! 
'''

message2 = '''
Hi Indika,

Today, our AI analyzed 120 new CT scans, helping doctors detect early signs of disease faster. 
User registrations increased by 15%, and system uptime remained at 99.9%. 
We successfully sent 200 report notifications. Our team continues optimizing algorithms for better accuracy and quicker turnaround times.


'''



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
    type = request_json['type']
    other_data = request_json['other_data']
    if type == 1:
        if send_email(email, "Welcome to our service!", message1):
            return f"Email successfully sent to {email}", 200

    elif type == 2:
        if send_email(email, "Daily update", message2):
            return f"Email successfully sent to {email}", 200

    elif type == 3:
        if send_email(email, "Report created", other_data):
            return f"Email successfully sent to {email}", 200
   
    return f"Failed to send email to {email}", 500

