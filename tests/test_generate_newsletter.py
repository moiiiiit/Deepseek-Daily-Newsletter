import pytest
from deepseek_daily_newsletter import generate_newsletter

def test_api_key_loading():
    key = generate_newsletter.load_api_key()
    assert isinstance(key, str)
    assert key.startswith('sk-')

def test_prompt_loading():
    model, prompt = generate_newsletter.load_prompt()
    assert isinstance(model, str)
    assert isinstance(prompt, str)
    assert 'Task:' in prompt
