from abc import ABC, abstractmethod
from typing import Iterable, Sized, TypeVar, Generic, Optional, Any
from uuid import UUID

from chatnoir.model.highlight import HighlightedText
from chatnoir.model.index import Index


class _Result(ABC):
    score: float
    uuid: UUID
    target_uri: str
    snippet: HighlightedText

    @property
    @abstractmethod
    def score(self) -> float:
        pass

    @property
    @abstractmethod
    def uuid(self) -> UUID:
        pass

    @property
    @abstractmethod
    def target_uri(self) -> str:
        pass

    @property
    @abstractmethod
    def snippet(self) -> HighlightedText:
        pass


# noinspection DuplicatedCode
class SearchResult(_Result):
    index: Index
    trec_id: Optional[str]
    target_hostname: str
    page_rank: Optional[float]
    spam_rank: Optional[float]
    title: HighlightedText
    explanation: Any

    @property
    @abstractmethod
    def index(self) -> Index:
        pass

    @property
    @abstractmethod
    def trec_id(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def target_hostname(self) -> str:
        pass

    @property
    @abstractmethod
    def page_rank(self) -> Optional[float]:
        pass

    @property
    @abstractmethod
    def spam_rank(self) -> Optional[float]:
        pass

    @property
    @abstractmethod
    def title(self) -> HighlightedText:
        pass

    @property
    @abstractmethod
    def explanation(self) -> Any:
        pass


class MinimalPhraseSearchResult(_Result, ABC):
    pass


# noinspection DuplicatedCode
class PhraseSearchResult(MinimalPhraseSearchResult):
    index: Index
    trec_id: Optional[str]
    target_hostname: str
    page_rank: Optional[float]
    spam_rank: Optional[float]
    title: HighlightedText
    explanation: Any

    @property
    @abstractmethod
    def index(self) -> Index:
        pass

    @property
    @abstractmethod
    def trec_id(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def target_hostname(self) -> str:
        pass

    @property
    @abstractmethod
    def page_rank(self) -> Optional[float]:
        pass

    @property
    @abstractmethod
    def spam_rank(self) -> Optional[float]:
        pass

    @property
    @abstractmethod
    def title(self) -> HighlightedText:
        pass

    @property
    @abstractmethod
    def explanation(self) -> Any:
        pass


class ResultsMeta(ABC):
    query_time: int
    total_results: int

    @property
    @abstractmethod
    def query_time(self) -> int:
        pass

    @property
    @abstractmethod
    def total_results(self) -> int:
        pass


ResultType = TypeVar("ResultType", bound=_Result)


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
