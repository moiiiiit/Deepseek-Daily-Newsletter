
import time
import threading
import schedule
import os
import json
from .generate_newsletters import generate_newsletters
from .send_email import send_email

# Cache sender_email and bcc_emails at module level
_sender_email = os.environ.get('SENDER_EMAIL')
_emails_json = os.environ.get('EMAILS_JSON')
if not _emails_json:
    raise ValueError("EMAILS_JSON not found in environment variables")
_recipients = json.loads(_emails_json)
_bcc_emails = [r['email'] for r in _recipients]

def job():
    generate_newsletters(send_email, _sender_email, _bcc_emails)

def setup_scheduler():
    schedule.every().monday.at("08:00").do(job)
    print("Scheduler job scheduled for Monday 8am.")

def run_scheduler():
    setup_scheduler()
    print("Scheduler started. Waiting for Monday 8am...")
    while True:
        schedule.run_pending()
        time.sleep(30)

def main():
    run_scheduler()

if __name__ == "__main__":
    main()
