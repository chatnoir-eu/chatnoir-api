from abc import ABC
from datetime import datetime
from typing import TypeVar, Generic, Optional, AbstractSet, Sequence
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
    lang: str


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


MetaType = TypeVar("MetaType", bound=Meta)
ResultType = TypeVar("ResultType", bound=MinimalResult)


class Results(
    Sequence[ResultType],
    Generic[MetaType, ResultType],
    ABC
):
    meta: MetaType
