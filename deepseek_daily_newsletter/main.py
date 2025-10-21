import time
import threading
import schedule
from .generate_newsletter import main as generate_newsletter
from .send_email import send_email

def job():
    # Generate newsletter and send email
    result = generate_newsletter()
    subject = "Weekly Deepseek EV Technology Digest"
    body = str(result)
    send_email(subject, body)


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
