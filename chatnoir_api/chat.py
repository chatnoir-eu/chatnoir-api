from json import dumps
from typing_extensions import Literal
from urllib.parse import urljoin

from requests import post

from chatnoir_api.constants import BASE_URL_CHAT

ModelType = Literal[
    "alpaca-en-7b",
    "gpt2-base",
    "gpt2-large",
    "gpt2-xl",
    "alpaca-en-7b-retrieve-clueweb22",
    "alpaca-en-7b-prompt-retrieve-rewritten-clueweb22",
    "gpt2-xl-rewrite-with-clueweb22",
]


def chat(
        api_key: str,
        input_sentence: str,
        model: ModelType = "alpaca-en-7b"
) -> str:
    url = urljoin(BASE_URL_CHAT, f"generate/{model}")
    data = dumps({
        "input_sentence": input_sentence,
    })
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Api-Key": api_key
    }
    response = post(url, data=data, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    if "response" not in response_json:
        raise ValueError(f"Invalid ChatNoir Chat response: {response_json}")
    return response_json["response"]
