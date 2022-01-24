from pytest import fixture

from chatnoir_api import HighlightedText


@fixture
def highlighted_text() -> HighlightedText:
    return HighlightedText("this is an <em>important</em> test")


@fixture
def text() -> str:
    return "this is an important test"


def test_highlighted_text(highlighted_text: HighlightedText, text: str):
    assert str(highlighted_text) == text
