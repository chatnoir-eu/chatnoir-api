from abc import ABC
from datetime import datetime
from typing import TypeVar, Generic, Optional, AbstractSet, Sequence, \
    overload, Union, Any, Iterator
from uuid import UUID

from chatnoir_api.cache import cache_contents
from chatnoir_api.model import Index
from chatnoir_api.model.highlight import HighlightedText


class MinimalResult(ABC):
    score: float
    uuid: UUID
    target_uri: str
    snippet: HighlightedText


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

    def cache_contents(self, plain: bool = False) -> str:
        return cache_contents(self.uuid, self.index, plain)


class ExplainedResult(Result, ExplainedMinimalResult, ABC):
    pass


class MinimalResultStaging(MinimalResult, ABC):
    index: Index
    title: HighlightedText

    def cache_contents(self, plain: bool = False) -> str:
        return cache_contents(self.uuid, self.index, plain)


class ExplainedMinimalResultStaging(
    MinimalResultStaging, ExplainedMinimalResult, ABC
):
    pass


class ResultStaging(MinimalResultStaging, Result, ABC):
    warc_id: Optional[str]
    cache_uri: str
    crawl_date: Optional[datetime]
    content_type: str
    language: str


class ExplainedResultStaging(ResultStaging, ExplainedResult, ABC):
    explanation: Explanation


class Meta(ABC):
    indices: AbstractSet[Index]
    query_time: int
    total_results: int


class MetaIndex(ABC):
    index: Index
    name: str
    selected: bool


class ExtendedMeta(Meta, ABC):
    indices: AbstractSet[MetaIndex]
    explain: bool
    max_page: int
    page_size: int
    query_string: str
    results_from: int
    results_to: int
    terminated_early: bool


_MetaType = TypeVar("_MetaType", bound=Meta)
_ResultType = TypeVar("_ResultType", bound=MinimalResult)


class Results(
    Sequence[_ResultType],
    Generic[_MetaType, _ResultType],
    ABC
):
    meta: _MetaType
    results: Sequence[_ResultType]


class ResultsMixin(
    Results[_MetaType, _ResultType],
    Generic[_MetaType, _ResultType],
    ABC
):
    meta: _MetaType
    results: Sequence[_ResultType]

    @overload
    def __getitem__(self, i: int) -> _ResultType:
        pass

    @overload
    def __getitem__(self, s: slice) -> Sequence[_ResultType]:
        pass

    def __getitem__(
            self,
            i: Union[int, slice],
    ) -> Union[_ResultType, Sequence[_ResultType]]:
        return self.results[i]

    def index(self, value: Any, start: int = ..., stop: int = ...) -> int:
        return self.results.index(value, start, stop)

    def count(self, value: Any) -> int:
        return self.results.count(value)

    def __contains__(self, x: object) -> bool:
        return x in self.results

    def __iter__(self) -> Iterator[_ResultType]:
        return iter(self.results)

    def __reversed__(self) -> Iterator[_ResultType]:
        return reversed(self.results)

    def __len__(self) -> int:
        return len(self.results)
