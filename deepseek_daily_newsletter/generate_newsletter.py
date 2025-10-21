import yaml
import json
import requests
import os

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

def load_api_key():
    path = os.path.join(STATIC_DIR, 'secrets.yaml')
    with open(path, 'r', encoding='utf-8') as f:
        secrets = yaml.safe_load(f)
    return secrets.get('Deepseek_private')

def load_prompt():
    path = os.path.join(STATIC_DIR, 'prompts.json')
    with open(path, 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    return prompts[0]['model'], prompts[0]['prompt']

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
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main():
    api_key = load_api_key()
    model, prompt = load_prompt()
    result = call_deepseek_api(api_key, model, prompt)
    print(result)

if __name__ == "__main__":
    main()
