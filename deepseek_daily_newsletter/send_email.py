import smtplib
import json
import yaml
import os
from email.message import EmailMessage

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

def send_email(subject, body):
    # Load sender email from static/secrets.yaml
    secrets_path = os.path.join(STATIC_DIR, 'secrets.yaml')
    with open(secrets_path, 'r', encoding='utf-8') as f:
        secrets = yaml.safe_load(f)
        sender_email = secrets.get('Deepseek_private')
        if not sender_email:
            raise ValueError("Sender email not found in static/secrets.yaml")

    # Load recipient emails from static/emails.json
    emails_path = os.path.join(STATIC_DIR, 'emails.json')
    with open(emails_path, 'r', encoding='utf-8') as f:
        recipients = json.load(f)
        bcc_emails = [r['email'] for r in recipients]

    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email  # To yourself
    msg['To'] = sender_email
    msg['Bcc'] = ', '.join(bcc_emails)
    msg.set_content(body)

    # Send the email (using localhost SMTP for example)
    with smtplib.SMTP('localhost') as server:
        server.send_message(msg)
