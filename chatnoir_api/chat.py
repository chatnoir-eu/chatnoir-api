from json import dumps, load
from urllib.parse import urljoin

from requests import post
from pathlib import Path

from chatnoir_api.constants import BASE_URL_CHAT
import os


def default_from_tira_environment(key):
    for potential_key in ['inputDataset', 'TIRA_INPUT_DATASET', 'CHATNOIR_CHAT_CONFIGURATION_DIR']:
        if not os.environ.get(potential_key, None):
            continue

        for file_name in ['metadata.json', '.chatnoir-settings.json']:
            try:
                ret = load(open(Path(os.environ.get(potential_key)) / file_name))
                return ret[key]
            except:
                pass


def default_from_environment(key, default=None):
    default_from_tira_env = default_from_tira_environment(key)

    if default_from_tira_env:
        return default_from_tira_env

    return os.environ.get(key, default)


class ChatNoirChatClient():
    def __init__(self, api_key=default_from_environment('chatnoir_chat_api_key'), model=default_from_environment('chatnoir_chat_model', 'alpaca-en-7b'), endpoint=default_from_environment('chatnoir_chat_endpoint', BASE_URL_CHAT)):
        self.api_key = api_key
        self.model = model
        self.endpoint = endpoint
        
        if not self.api_key:
            raise ValueError('Please provide a proper api_key, got: ' + str(self.api_key))

        if not self.model:
            raise ValueError('Please provide a proper model, got: ' + str(self.api_key))

        if not self.endpoint:
            raise ValueError('Please provide a proper model, got: ' + str(self.api_key))

    def chat(self, input_sentence: str) -> str:
        url = urljoin(BASE_URL_CHAT, f"generate/{self.model}")
        data = dumps({"input_sentence": input_sentence})
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Api-Key": self.api_key
        }
    
        response = post(url, data=data, headers=headers)
        response.raise_for_status()
        response_json = response.json()

        if "response" not in response_json:
            raise ValueError(f"Invalid ChatNoir Chat response: {response_json}")
        return response_json["response"]

