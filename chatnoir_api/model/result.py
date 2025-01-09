from abc import ABC, abstractmethod
from datetime import datetime
from typing import (
    TypeVar,
    Generic,
    Optional,
    AbstractSet,
    Sequence,
    overload,
    Union,
    Any,
    Iterator,
    final
)
from uuid import UUID

from chatnoir_api.cache import cache_contents
from chatnoir_api.model import Index, SearchMethod
from chatnoir_api.model.highlight import HighlightedText


class MinimalResult(ABC):
    score: float
    uuid: UUID
    target_uri: Optional[str]
    snippet: HighlightedText
    index: Index
    title: HighlightedText

    def cache_contents(self, plain: bool = False) -> str:
        return cache_contents(self.uuid, self.index, plain)


class Explanation(ABC):
    value: float
    description: str
    details: Sequence["Explanation"]


class ExplainedMinimalResult(MinimalResult, ABC):
    explanation: Explanation


class Result(MinimalResult, ABC):
    index: Index
    trec_id: Optional[str]
    target_hostname: str
    page_rank: Optional[float]
    spam_rank: Optional[float]
    title: HighlightedText
    warc_id: Optional[str]
    cache_uri: str
    crawl_date: Optional[datetime]
    content_type: Optional[str]
    language: str


class ExplainedResult(Result, ExplainedMinimalResult, ABC):
    pass


class Meta(ABC):
    indices: AbstractSet[Index]
    query_time: int
    total_results: int
    search_method: SearchMethod


class MetaIndex(ABC):
    index: Index
    name: str
    selected: bool


class ExtendedMeta(Meta, ABC):
    indices: AbstractSet[MetaIndex]  # type: ignore
    explain: bool
    max_page: int
    page_size: int
    query_string: str
    results_from: int
    results_to: int
    terminated_early: bool


_MetaType = TypeVar("_MetaType", bound=Meta, covariant=True)
_ResultType = TypeVar("_ResultType", bound=MinimalResult, covariant=True)


class Results(Sequence[_ResultType], Generic[_MetaType, _ResultType], ABC):
    @property
    @abstractmethod
    def meta(self) -> _MetaType:
        pass

    @property
    @abstractmethod
    def results(self) -> Sequence[_ResultType]:
        pass


class ResultsMixin(
    Results[_MetaType, _ResultType], Generic[_MetaType, _ResultType], ABC
):
    _meta: _MetaType
    _results: Sequence[_ResultType]

    @property
    def meta(self) -> _MetaType:
        return self._meta

    @property
    def results(self) -> Sequence[_ResultType]:
        return self._results

    @overload
    def __getitem__(self, i: int) -> _ResultType:
        pass

    @overload
    def __getitem__(self, s: slice) -> Sequence[_ResultType]:
        pass

    @final
    def __getitem__(
        self,
        i: Union[int, slice],
    ) -> Union[_ResultType, Sequence[_ResultType]]:
        return self.results[i]

    @final
    def index(self, value: Any, start: int = 0, stop: int = -1) -> int:
        return self.results.index(value, start, stop)

    @final
    def count(self, value: Any) -> int:
        return self.results.count(value)

    @final
    def __contains__(self, x: object) -> bool:
        return x in self.results

    @final
    def __iter__(self) -> Iterator[_ResultType]:
        return iter(self.results)

    @final
    def __reversed__(self) -> Iterator[_ResultType]:
        return reversed(self.results)

    @final
    def __len__(self) -> int:
        return len(self.results)
