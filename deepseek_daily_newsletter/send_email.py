import smtplib
from email.message import EmailMessage

def send_email(subject, body, sender_email, bcc_emails):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = sender_email
    msg['Bcc'] = ', '.join(bcc_emails)
    msg.set_content(body)

    with smtplib.SMTP('localhost') as server:
        server.send_message(msg)
