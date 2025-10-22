from .logger import logger

import time
import threading
import schedule
import os
import json
from .generate_newsletters import generate_newsletters
from .send_email import send_email
import base64

# Cache sender_email and bcc_emails at module level
_sender_email_b64 = os.environ.get('SENDER_EMAIL')
if not _sender_email_b64:
    raise ValueError("SENDER_EMAIL not found in environment variables")
_sender_email = base64.b64decode(_sender_email_b64).decode('utf-8')
_emails_json_b64 = os.environ.get('EMAILS_JSON')
if not _emails_json_b64:
    raise ValueError("EMAILS_JSON not found in environment variables")
_emails_json = base64.b64decode(_emails_json_b64).decode('utf-8')
_recipients = json.loads(_emails_json)
_bcc_emails = [r['email'] for r in _recipients]

def job():
    generate_newsletters(send_email, _sender_email, _bcc_emails)

def setup_scheduler():
    schedule.every().monday.at("08:00").do(job)
    logger.info("Scheduler job scheduled for Monday 8am.")

def run_scheduler():
    setup_scheduler()
    logger.info("Scheduler started. Waiting for Monday 8am...")
    while True:
        schedule.run_pending()
        time.sleep(30)

def main():
    run_scheduler()

if __name__ == "__main__":
    import sys
    if "--run-now" in sys.argv:
        from .generate_newsletters import generate_newsletters
        from .send_email import send_email
        generate_newsletters(send_email, _sender_email, _bcc_emails)
    else:
        main()
