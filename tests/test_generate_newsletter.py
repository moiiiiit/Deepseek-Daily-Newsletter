import dotenv
dotenv.load_dotenv(dotenv_path=".env.test")
import pytest
import requests_mock
from deepseek_daily_newsletter import generate_newsletters
import json

def test_api_key_loading():
    key = generate_newsletters.load_api_key()
    assert isinstance(key, str)
    assert key.startswith('sk-')

def test_prompt_loading():
    model, prompt = generate_newsletters.load_prompts()
    assert model
    assert prompt

def test_env_prompt_loading(monkeypatch):
    prompts = [
        {"model": "model1", "prompt": "prompt1"},
        {"model": "model2", "prompt": "prompt2"}
    ]
    monkeypatch.setenv("PROMPTS_JSON", json.dumps(prompts))
    loaded = generate_newsletters.load_prompts()
    assert loaded == prompts

def test_generate_newsletters(monkeypatch):
    sent = []
    def dummy_send_email(subject, body, sender_email, bcc_emails):
        sent.append((subject, body, sender_email, bcc_emails))
    with requests_mock.Mocker() as m:
        m.post("https://api.deepseek.com/v1/chat/completions", json={"result": "mocked"})
        generate_newsletters.generate_newsletters(dummy_send_email, "sender@example.com", ["a@example.com"])
    assert len(sent) == 2
    assert sent[0][0].startswith("Newsletter for model:")
