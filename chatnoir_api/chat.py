from json import load
from urllib.parse import urljoin

from pathlib import Path

from chatnoir_api.constants import BASE_URL_CHAT, BASE_URL_CHAT_SOCKET
from chatnoir_api.v1.requests import request_page
from dataclasses_json import DataClassJsonMixin
from chatnoir_api.v1.defaults import (DEFAULT_RETRIES, DEFAULT_BACKOFF_SECONDS)
from dataclasses import dataclass
import os
import time
import json
import threading


def chat(api_key, input_sentence, model='alpaca-en-7b'):
    return ChatNoirChatClient(api_key=api_key, model=model)


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
    text_request: str
    seed: str


@dataclass(frozen=True)
class ChatResponse(DataClassJsonMixin):
    response: str


class ChatNoirChatClient():
    def __init__(self,
                 api_key=default_config('chatnoir_chat_api_key'),
                 model=default_config('chatnoir_chat_model', 'alpaca-en-7b'),
                 endpoint=default_config(
                                         'chatnoir_chat_endpoint',
                                         BASE_URL_CHAT
                                        ),
                 ws_host=default_config(
                                        'chatnoir_chat_ws_endpoint',
                                        BASE_URL_CHAT_SOCKET
                                       ),
                 retries=DEFAULT_RETRIES,
                 backoff_seconds=DEFAULT_BACKOFF_SECONDS,
                 ):

        self.retries = retries
        self.backoff_seconds = backoff_seconds

        if type(ws_host) == tuple:
            print(f"ChatNoir Chat uses ws_host from environment {ws_host[1]}")
            self.ws_host = ws_host[0]
        else:
            self.ws_host = ws_host
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

    def chat(self, text_request: str, seed: str = "0") -> str:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Api-Key": self.api_key
        }
        url = urljoin(self.endpoint, f"seq2seq/{self.model}")

        response = request_page(
                request=ChatRequest(text_request, seed),
                response_type=ChatResponse,
                endpoint='chat',
                url_for_request=url,
                non_default_headers=headers,
                retries=self.retries,
                backoff_seconds=self.backoff_seconds
        )

        return response.response

    def serve_chat_backend(self,
                           backend_id,
                           backend_implementation,
                           in_backend_thread=False,
                           failsave=True
                           ):
        from websocket import create_connection
        if in_backend_thread:
            def thread_method():
                self.serve_chat_backend(backend_id, backend_implementation)

            threading.Thread(
                target=thread_method,
                name="serve_chat_backend_thread",
                daemon=True
            ).start()
            time.sleep(.05)
            return

        while True:
            try:
                print('Will connect to ' + str(self.ws_host), flush=True)
                ws = create_connection(self.ws_host)
                ws.send(json.dumps({'backend_id': backend_id}))
                print('Done. Connected to ' + str(self.ws_host), flush=True)

                while True:
                    result = json.loads(ws.recv())
                    ret = backend_implementation(result['text'])
                    init_message = json.dumps({
                                               'uuid': result['uuid'],
                                               'text': ret,
                                               'backend_id': backend_id
                                              })

                    ws.send(init_message)
            except Exception as e:
                print('Restart loop because of error ' + str(e))
                if not failsave:
                    raise e
