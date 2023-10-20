from pytest import fixture

from chatnoir_api.chat import ChatNoirChatClient


@fixture(scope="module", params=[
    "alpaca-en-7b",
    "gpt2-xl"
])
def model(request) -> str:
    return request.param


def test_chat(model: str) -> None:
    input_sentence = "Please repeat the word \"test\"."
    response = ChatNoirChatClient().chat(input_sentence)

    assert response is not None
    assert isinstance(response, str)
    assert "test" in response.casefold()
