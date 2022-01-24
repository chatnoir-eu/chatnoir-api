from abc import ABC
from typing import TypeVar, Generic, Optional, Sequence
from uuid import UUID

from chatnoir_api.html import html_contents
from chatnoir_api.model import Index
from chatnoir_api.model.highlight import HighlightedText


class Result(ABC):
    score: float = NotImplemented
    uuid: UUID = NotImplemented
    target_uri: str = NotImplemented
    snippet: HighlightedText = NotImplemented


# noinspection DuplicatedCode
class SearchResult(Result):
    index: Index = NotImplemented
    trec_id: Optional[str] = NotImplemented
    target_hostname: str = NotImplemented
    page_rank: Optional[float] = NotImplemented
    spam_rank: Optional[float] = NotImplemented
    title: HighlightedText = NotImplemented
    explanation: Optional[dict] = NotImplemented

    def html_contents(self, plain: bool = False) -> str:
        return html_contents(self.uuid, self.index, plain)


class MinimalPhraseSearchResult(Result, ABC):
    pass


# noinspection DuplicatedCode
class PhraseSearchResult(MinimalPhraseSearchResult):
    index: Index = NotImplemented
    trec_id: Optional[str] = NotImplemented
    target_hostname: str = NotImplemented
    page_rank: Optional[float] = NotImplemented
    spam_rank: Optional[float] = NotImplemented
    title: HighlightedText = NotImplemented
    explanation: Optional[dict] = NotImplemented

    def html_contents(self, plain: bool = False) -> str:
        return html_contents(self.uuid, self.index, plain)


class ResultsMeta(ABC):
    query_time: int = NotImplemented
    total_results: int = NotImplemented


ResultType = TypeVar("ResultType", bound=Result)


class Results(
    Sequence[ResultType],
    ResultsMeta,
    Generic[ResultType],
    ABC
):
    pass
