import requests
import json


def chat(api_key: str, input_sentence: str, model: str = 'alpaca-en-7b'):
    url = f'https://chat.web.webis.de/generate/{model}'
    data = json.dumps({"input_sentence": input_sentence})
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Api-Key": api_key
    }
    response = requests.post(url, data=data, headers=headers)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()['response']
