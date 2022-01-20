from abc import ABC
from dataclasses import dataclass, field
from typing import List
from typing import Optional, Set
from uuid import UUID

from dataclasses_json import config, DataClassJsonMixin

from chatnoir_api.model import Index, Slop
from chatnoir_api.model.highlight import HighlightedText
from chatnoir_api.model.result import (
    ResultsMeta, SearchResult, PhraseSearchResult, MinimalPhraseSearchResult
)


@dataclass(frozen=True)
class Request(DataClassJsonMixin):
    apikey: str
    query: str
    index: Set[Index] = field(metadata=config(
        encoder=lambda indices: {index.value for index in indices},
        decoder=lambda indices: {Index(index) for index in indices}
    ))
    start: Optional[int] = field(metadata=config(field_name="from"))
    size: Optional[int]
    explain: bool


@dataclass(frozen=True)
class SearchRequest(Request, DataClassJsonMixin):
    pass


@dataclass(frozen=True)
class PhraseSearchRequest(Request, DataClassJsonMixin, ABC):
    slop: Optional[Slop]
    minimal: bool = False


@dataclass(frozen=True)
class ResponseMeta(ResultsMeta, DataClassJsonMixin):
    indices: Set[Index] = field(metadata=config(
        encoder=lambda indices: {index.value for index in indices},
        decoder=lambda indices: {Index(index) for index in indices}
    ))
    query_time: int
    total_results: int


@dataclass(frozen=True)
class ResponseResult(DataClassJsonMixin):
    score: float
    uuid: UUID
    target_uri: str
    snippet: HighlightedText = field(metadata=config(
        encoder=str,
        decoder=HighlightedText
    ))


@dataclass(frozen=True)
class SearchResponseResult(ResponseResult, SearchResult, DataClassJsonMixin):
    index: Index = field(metadata=config(
        encoder=str,
        decoder=Index
    ))
    title: HighlightedText = field(metadata=config(
        encoder=str,
        decoder=HighlightedText,
    ))
    trec_id: Optional[str]
    target_hostname: str
    page_rank: Optional[float]
    spam_rank: Optional[float]
    explanation: Optional[dict]


@dataclass(frozen=True)
class MinimalPhraseSearchResponseResult(
    ResponseResult,
    MinimalPhraseSearchResult,
    DataClassJsonMixin
):
    pass


@dataclass(frozen=True)
class PhraseSearchResponseResult(
    MinimalPhraseSearchResponseResult,
    PhraseSearchResult,
    DataClassJsonMixin
):
    index: Index = field(metadata=config(
        encoder=str,
        decoder=Index
    ))
    title: HighlightedText = field(metadata=config(
        encoder=str,
        decoder=HighlightedText
    ))
    trec_id: Optional[str]
    target_hostname: str
    page_rank: Optional[float]
    spam_rank: Optional[float]
    explanation: Optional[dict]


@dataclass(frozen=True)
class Response(DataClassJsonMixin):
    meta: ResponseMeta
    results: List[ResponseResult]


@dataclass(frozen=True)
class SearchResponse(Response, DataClassJsonMixin):
    results: List[SearchResponseResult]


@dataclass(frozen=True)
class MinimalPhraseSearchResponse(Response, DataClassJsonMixin):
    results: List[MinimalPhraseSearchResponseResult]


@dataclass(frozen=True)
class PhraseSearchResponse(Response, DataClassJsonMixin):
    results: List[PhraseSearchResponseResult]
