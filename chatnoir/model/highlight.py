from dataclasses import dataclass
from functools import cached_property
from html.parser import HTMLParser
from parser import ParserError
from typing import List, Union, Optional

from chatnoir import logger


class Highlight(str):
    pass


@dataclass
class HighlightedText(str):
    html: str

    @cached_property
    def text(self) -> str:
        return "".join(self.sequence)

    @cached_property
    def sequence(self) -> List[Union[str, Highlight]]:
        parser = _HighlightParser()
        parser.feed(self.html)
        sequence = parser.sequence
        parser.close()
        return sequence


class _HighlightParser(HTMLParser):
    sequence: List[Union[str, Highlight]] = []
    _current_data: Optional[str] = None

    def handle_starttag(self, tag: str, attrs):
        if tag != "em":
            raise ParserError("Can only parse <em> tags.")
        if attrs:
            raise ParserError("Cannot parse attributes.")
        if self._current_data is not None:
            self.sequence.append(self._current_data)
            self._current_data = None
        else:
            logger.warning("Empty non-hightlight string.")

    # Overridable -- handle end tag
    def handle_endtag(self, tag: str):
        if tag != "em":
            raise ParserError("Can only parse <em> tags.")
        if self._current_data is not None:
            self.sequence.append(Highlight(self._current_data))
            self._current_data = None
        else:
            logger.warning("Empty hightlight string.")

    def handle_charref(self, name: str):
        raise ParserError("Can only parse <em> tags.")

    def handle_entityref(self, name: str):
        raise ParserError("Can only parse <em> tags.")

    def handle_data(self, data: str):
        raise ParserError("Can only parse <em> tags.")

    def handle_comment(self, data: str):
        raise ParserError("Can only parse <em> tags.")

    def handle_decl(self, decl: str):
        raise ParserError("Can only parse <em> tags.")

    def handle_pi(self, data: str):
        raise ParserError("Can only parse <em> tags.")
