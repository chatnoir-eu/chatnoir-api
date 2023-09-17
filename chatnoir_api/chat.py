from json import dumps, load
from urllib.parse import urljoin

from requests import post
from pathlib import Path

from chatnoir_api.constants import BASE_URL_CHAT
from chatnoir_api.v1.requests import request_page
from dataclasses_json import config, DataClassJsonMixin
from chatnoir_api.v1.defaults import (DEFAULT_RETRIES, DEFAULT_BACKOFF_SECONDS)
from dataclasses import dataclass
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

@dataclass(frozen=True)
class ChatRequest(DataClassJsonMixin):
    input_sentence: str
    
@dataclass(frozen=True)
class ChatResponse(DataClassJsonMixin):
    response: str

class ChatNoirChatClient():
    def __init__(self,
                 api_key=default_config('chatnoir_chat_api_key'),
                 model=default_config('chatnoir_chat_model', 'alpaca-en-7b'),
                 endpoint=default_config('chatnoir_chat_endpoint', BASE_URL_CHAT),
                 retries=DEFAULT_RETRIES,
                 backoff_seconds=DEFAULT_BACKOFF_SECONDS,
                 ):

        self.retries = retries
        self.backoff_seconds = backoff_seconds

        if type(api_key) == tuple:
            print(f"ChatNoir Chat uses API key from {api_key[1]}")
            self.api_key = api_key[0]
        else:
            print("ChatNoir Chat uses API key from parameters")
            self.api_key = api_key

        if type(model) == tuple:
            print(f"ChatNoir Chat uses model '{model[0]}' from {model[1]}")
            self.model = model[0]
        else:
            print("ChatNoir Chat uses model '{model}' from from parameters")
            self.model = model
        
        if type(endpoint) == tuple:
            print(f"ChatNoir Chat uses endpoint '{endpoint[0]}' " +
                   "from {endpoint[1]}")
            self.endpoint = endpoint[0]
        else:
            print(f"ChatNoir Chat uses endpoint '{endpoint}' " +
                   "from parameters")
            self.endpoint = endpoint

    def chat(self, input_sentence: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Api-Key": self.api_key
        }

        response = request_page(
                request=ChatRequest(input_sentence),
                response_type=ChatResponse,
                endpoint='chat',
                url_for_request=urljoin(BASE_URL_CHAT, f"generate/{self.model}"),
                non_default_headers=headers, 
                retries=self.retries,
                backoff_seconds=self.backoff_seconds
        )
        
        return response.response
