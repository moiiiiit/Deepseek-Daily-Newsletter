from .logger import logger
import smtplib
from email.message import EmailMessage

def send_email(subject, body, sender_email, bcc_emails):
    logger.info(f"Preparing email: subject={subject}, sender={sender_email}, bcc={bcc_emails}")
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = sender_email
    msg['Bcc'] = ', '.join(bcc_emails)
    msg.set_content(body)

    try:
        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
        logger.info(f"Email sent to {bcc_emails}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
