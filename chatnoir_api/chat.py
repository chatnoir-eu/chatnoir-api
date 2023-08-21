from json import dumps, load
from urllib.parse import urljoin

from requests import post
from pathlib import Path

from chatnoir_api.constants import BASE_URL_CHAT
import os


def default_from_tira_environment(key):
    ENVIRONMENT_LOOKUP_KEYS = ['inputDataset', 'TIRA_INPUT_DATASET',
                               'CHATNOIR_CHAT_CONFIGURATION_DIR']

    for potential_key in ENVIRONMENT_LOOKUP_KEYS:
        if not os.environ.get(potential_key, None):
            continue

        for file_name in ['metadata.json', '.chatnoir-settings.json']:
            ret = load(open(Path(os.environ.get(potential_key)) / file_name))
            return ret[key], f'Configuration file "{file_name}"'


def default_config(key, default=None):
    default_from_tira_env = default_from_tira_environment(key)

    if default_from_tira_env:
        return default_from_tira_env

    return os.environ.get(key, default), "Environment variable"

default_api_key = 


class ChatNoirChatClient():
    def __init__(self,
                 api_key=default_config('chatnoir_chat_api_key'),
                 model=default_config('chatnoir_chat_model', 'alpaca-en-7b'),
                 endpoint=default_config('chatnoir_chat_endpoint', BASE_URL_CHAT)):

        if type(api_key) == tuple:
            print(f"ChatNoir Chat uses API key from {api_key[1]}")
            self.api_key = api_key[0]
        else:
            print(f"ChatNoir Chat uses API key from from parameters")
            self.api_key = api_key

        if type(self.model) == tuple:
            print(f"ChatNoir Chat uses model '{model[0]}' from {self.model[1]}")
            self.model = model[0]
        else:
            print(f"ChatNoir Chat uses model '{model}' from from parameters")
            self.model = model
        
        if type(self.endpoint) == tuple:
            print(f"ChatNoir Chat uses endpoint '{endpoint[0]}' from {self.endpoint[1]}")
            self.endpoint = endpoint[0]
        else:
            print(f"ChatNoir Chat uses model '{endpoint}' from from parameters")
            self.endpoint = endpoint

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
            raise ValueError(f"Invalid ChatNoir response: {response_json}")
        return response_json["response"]
