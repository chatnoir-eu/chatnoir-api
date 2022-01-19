from abc import ABC
from typing import Iterable, Sized, TypeVar, Generic, Optional, Any, Dict
from uuid import UUID

from chatnoir.model.highlight import HighlightedText
from chatnoir.model.index import Index


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
    explanation: Optional[Dict] = NotImplemented


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
    explanation: Optional[Dict] = NotImplemented


class ResultsMeta(ABC):
    query_time: int = NotImplemented
    total_results: int = NotImplemented


ResultType = TypeVar("ResultType", bound=Result)


class Results(
    Sized,
    Iterable[ResultType],
    Generic[ResultType],
    ResultsMeta,
    ABC
):
    def __len__(self) -> int:
        return self.total_results


class SearchResults(Results[SearchResult], ABC):
    pass


class MinimalPhraseSearchResults(Results[MinimalPhraseSearchResult], ABC):
    pass


class PhraseSearchResults(Results[PhraseSearchResult], ABC):
    pass
