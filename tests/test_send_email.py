import pytest
from deepseek_daily_newsletter import send_email

def test_send_email_function_exists():
    assert callable(send_email.send_email)
