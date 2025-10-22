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
    import base64
    prompts = [
        {"model": "model1", "prompt": "prompt1"},
        {"model": "model2", "prompt": "prompt2"}
    ]
    encoded = base64.b64encode(json.dumps(prompts).encode('utf-8')).decode('utf-8')
    monkeypatch.setenv("PROMPTS_JSON", encoded)
    loaded = generate_newsletters.load_prompts()
    assert loaded == prompts

def test_generate_newsletters(monkeypatch):
    sent = []
    def dummy_send_email(subject, body, sender_email, bcc_emails):
        sent.append((subject, body, sender_email, bcc_emails))
    import base64
    prompts = [
        {"model": "model1", "prompt": "prompt1"},
        {"model": "model2", "prompt": "prompt2"}
    ]
    encoded = base64.b64encode(json.dumps(prompts).encode('utf-8')).decode('utf-8')
    monkeypatch.setenv("PROMPTS_JSON", encoded)
    monkeypatch.setenv("SENDER_EMAIL", base64.b64encode("sender@example.com".encode('utf-8')).decode('utf-8'))
    with requests_mock.Mocker() as m:
        m.post("https://api.deepseek.com/v1/chat/completions", json={"result": "mocked"})
        generate_newsletters.generate_newsletters(dummy_send_email, "sender@example.com", ["a@example.com"])
    assert len(sent) == 2
    assert sent[0][0].startswith("Newsletter for model:")
