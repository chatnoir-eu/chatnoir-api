from dataclasses import dataclass
from html.parser import HTMLParser
from typing import List, Union, Optional

from chatnoir.api import logger
from chatnoir.api.types import cached_property


class Highlight(str):
    pass


@dataclass(frozen=True)
class HighlightedText(str):
    html: str

    def __str__(self) -> str:
        return "".join(self.sequence)

    @cached_property
    def sequence(self) -> List[Union[str, Highlight]]:
        parser = _HighlightParser()
        parser.feed(self.html)
        sequence = parser.sequence
        parser.close()
        return sequence


class _HighlightParser(HTMLParser):
    _current_sequence: List[Union[str, Highlight]] = []
    _current_data: Optional[str] = None
    _current_is_highlight = False

    def __init__(self):
        super().__init__(convert_charrefs=True)

    @property
    def sequence(self) -> List[Union[str, Highlight]]:
        sequence = self._current_sequence
        if self._current_data is not None:
            sequence.append(self._current_data)
        return sequence

    def handle_starttag(self, tag: str, attrs):
        if tag != "em":
            print(1)
            raise SyntaxError("Can only parse <em> tags.")
        if attrs:
            print(2)
            raise SyntaxError("Cannot parse attributes.")
        if self._current_is_highlight:
            raise SyntaxError("Nested <em> tags are not supported.")
        if self._current_data is not None:
            self._current_sequence.append(self._current_data)
            self._current_data = None
            self._current_is_highlight = True
        else:
            logger.warning("Empty non-hightlight string.")

    # Overridable -- handle end tag
    def handle_endtag(self, tag: str):
        if tag != "em":
            print(3)
            raise SyntaxError("Can only parse <em> tags.")
        if not self._current_is_highlight:
            raise SyntaxError("Nested <em> tags are not supported.")
        if self._current_data is not None:
            self._current_sequence.append(Highlight(self._current_data))
            self._current_data = None
            self._current_is_highlight = False
        else:
            logger.warning("Empty highlight string.")

    def handle_charref(self, name: str):
        raise AssertionError(
            "Should never be called because convert_charrefs is True."
        )

    def handle_entityref(self, name: str):
        raise AssertionError(
            "Should never be called because convert_charrefs is True."
        )

    def handle_data(self, data: str):
        self._current_data = data

    def handle_comment(self, data: str):
        raise SyntaxError("Comments are not supported.")

    def handle_decl(self, decl: str):
        print(8)
        raise SyntaxError("Doctype declarations are not supported.")

    def handle_pi(self, data: str):
        print(9)
        raise SyntaxError("Processing instructions are not supported.")
