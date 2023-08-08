from pytest import fixture

from chatnoir_api.chat import chat


@fixture(scope="module", params=[
    "alpaca-en-7b",
    "gpt2-base",
    "gpt2-large",
    "gpt2-xl",
    "alpaca-en-7b-retrieve-clueweb22",
    "alpaca-en-7b-prompt-retrieve-rewritten-clueweb22",
    "gpt2-xl-rewrite-with-clueweb22",
])
def model(request) -> str:
    return request.param


def test_chat(api_key_chat: str, model: str) -> None:
    input_sentence = "Please repeat the word \"test\"."
    response = chat(api_key_chat, input_sentence)

    assert response is not None
    assert isinstance(response, str)
    assert "test" in response.casefold()
