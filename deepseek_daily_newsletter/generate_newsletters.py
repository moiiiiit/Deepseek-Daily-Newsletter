from .logger import logger
import yaml
import json
import requests
import os

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

def load_api_key():
    return os.environ.get('DEEPSEEK_API_KEY')

def load_prompts():
    prompts_json = os.environ.get('PROMPTS_JSON')
    if not prompts_json:
        raise ValueError("PROMPTS_JSON not found in environment variables")
    return json.loads(prompts_json)

def call_deepseek_api(api_key, model, prompt):
    url = 'https://api.deepseek.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': model,
        'messages': [
            {'role': 'user', 'content': prompt}
        ]
    }
    logger.info(f"Calling Deepseek API with model={model}")
    response = requests.post(url, headers=headers, json=data)
    try:
        response.raise_for_status()
        logger.info("Deepseek API call successful")
    except Exception as e:
        logger.error(f"Deepseek API call failed: {e}")
        raise
    return response.json()


# This function generates newsletters for all prompts and sends emails for each
def generate_newsletters(send_email_func, sender_email, bcc_emails):
    api_key = load_api_key()
    prompts = load_prompts()
    for item in prompts:
        model = item['model']
        prompt = item['prompt']
        logger.info(f"Generating newsletter for model={model}")
        result = call_deepseek_api(api_key, model, prompt)
        subject = f"Newsletter for model: {model}"
        body = str(result)
        send_email_func(subject, body, sender_email, bcc_emails)
        logger.info(f"Newsletter sent for model={model}")
