from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Sequence, Set
from uuid import UUID

from dataclasses_json import config, DataClassJsonMixin

from chatnoir_api.model import Index, Slop, decode_uuid, index_id, parse_index, SearchMethod
from chatnoir_api.model.highlight import HighlightedText
from chatnoir_api.model.result import (
    Meta,
    Result,
    ExtendedMeta,
    MetaIndex,
    MinimalResult,
    ExplainedMinimalResult,
    Explanation,
    ExplainedResult,
    ResultsMixin,
)


@dataclass(frozen=True)
class Request(DataClassJsonMixin):
    apikey: str
    query: str
    index: Set[Index] = field(
        metadata=config(encoder=lambda indices: {index_id(index) for index in indices})
    )
    start: Optional[int] = field(metadata=config(field_name="from"))
    size: Optional[int]
    explain: bool
    minimal: bool
    extended_meta: bool
    search_method: SearchMethod


@dataclass(frozen=True)
class PhraseRequest(Request, DataClassJsonMixin):
    slop: Optional[Slop]


@dataclass(frozen=True)
class MinimalResultResponse(MinimalResult, DataClassJsonMixin):
    score: float
    uuid: UUID = field(metadata=config(decoder=decode_uuid))
    target_uri: Optional[str]
    snippet: HighlightedText = field(metadata=config(decoder=HighlightedText))
    index: Index = field(metadata=config(decoder=parse_index))
    title: HighlightedText = field(
        metadata=config(
            encoder=str,
            decoder=HighlightedText,
        )
    )


@dataclass(frozen=True)
class ExplanationResponse(Explanation, DataClassJsonMixin):
    value: float
    description: str
    details: Sequence["Explanation"]


@dataclass(frozen=True)
class ExplainedMinimalResultResponse(
    MinimalResultResponse, ExplainedMinimalResult, DataClassJsonMixin
):
    explanation: ExplanationResponse


def _decode_datetime(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value)


@dataclass(frozen=True)
class ResultResponse(MinimalResultResponse, Result, DataClassJsonMixin):
    index: Index = field(metadata=config(decoder=parse_index))
    trec_id: Optional[str]
    target_hostname: str
    page_rank: Optional[float]
    spam_rank: Optional[float]
    title: HighlightedText = field(metadata=config(decoder=HighlightedText))
    warc_id: Optional[str]
    cache_uri: str
    crawl_date: Optional[datetime] = field(metadata=config(decoder=_decode_datetime))
    content_type: Optional[str]
    language: str = field(metadata=config(field_name="lang"))


@dataclass(frozen=True)
class ExplainedResultResponse(
    ResultResponse, ExplainedMinimalResultResponse, ExplainedResult, DataClassJsonMixin
):
    explanation: ExplanationResponse


@dataclass(frozen=True)
class MetaResponse(Meta, DataClassJsonMixin):
    indices: Set[Index] = field(
        metadata=config(decoder=lambda ids: {parse_index(id) for id in ids})
    )
    query_time: int
    total_results: int
    search_method: SearchMethod


@dataclass(frozen=True)
class MetaIndexResponse(MetaIndex, DataClassJsonMixin):
    index: Index = field(
        metadata=config(
            decoder=parse_index,
            field_name="id",
        )
    )
    name: str
    selected: bool


@dataclass(frozen=True)
class ExtendedMetaResponse(MetaResponse, ExtendedMeta, DataClassJsonMixin):
    indices: Set[MetaIndexResponse]  # type: ignore
    explain: bool
    max_page: int
    page_size: int
    query_string: str
    results_from: int
    results_to: int
    terminated_early: bool


@dataclass(frozen=True)
class MinimalSearchResponse(
    DataClassJsonMixin, ResultsMixin[MetaResponse, MinimalResultResponse]
):
    _meta: MetaResponse = field(metadata=config(field_name="meta"))
    _results: Sequence[MinimalResultResponse] = field(metadata=config(field_name="results"))


@dataclass(frozen=True)
class ExplainedMinimalSearchResponse(
    DataClassJsonMixin, ResultsMixin[MetaResponse, MinimalResultResponse]
):
    _meta: MetaResponse = field(metadata=config(field_name="meta"))
    _results: Sequence[ExplainedMinimalResultResponse] = field(metadata=config(field_name="results"))


@dataclass(frozen=True)
class SearchResponse(
    DataClassJsonMixin, ResultsMixin[MetaResponse, MinimalResultResponse]
):
    _meta: MetaResponse = field(metadata=config(field_name="meta"))
    _results: Sequence[ResultResponse] = field(metadata=config(field_name="results"))


@dataclass(frozen=True)
class ExplainedSearchResponse(
    DataClassJsonMixin, ResultsMixin[MetaResponse, MinimalResultResponse]
):
    _meta: MetaResponse = field(metadata=config(field_name="meta"))
    _results: Sequence[ExplainedResultResponse] = field(metadata=config(field_name="results"))


@dataclass(frozen=True)
class ExtendedMetaMinimalSearchResponse(
    DataClassJsonMixin, ResultsMixin[MetaResponse, MinimalResultResponse]
):
    _meta: ExtendedMetaResponse = field(metadata=config(field_name="meta"))
    _results: Sequence[MinimalResultResponse] = field(metadata=config(field_name="results"))


@dataclass(frozen=True)
class ExplainedExtendedMetaMinimalSearchResponse(
    DataClassJsonMixin, ResultsMixin[MetaResponse, MinimalResultResponse]
):
    _meta: ExtendedMetaResponse = field(metadata=config(field_name="meta"))
    _results: Sequence[ExplainedMinimalResultResponse] = field(metadata=config(field_name="results"))


@dataclass(frozen=True)
class ExtendedMetaSearchResponse(
    DataClassJsonMixin, ResultsMixin[MetaResponse, MinimalResultResponse]
):
    _meta: ExtendedMetaResponse = field(metadata=config(field_name="meta"))
    _results: Sequence[ResultResponse] = field(metadata=config(field_name="results"))


@dataclass(frozen=True)
class ExplainedExtendedMetaSearchResponse(
    DataClassJsonMixin, ResultsMixin[MetaResponse, MinimalResultResponse]
):
    _meta: ExtendedMetaResponse = field(metadata=config(field_name="meta"))
    _results: Sequence[ExplainedResultResponse] = field(metadata=config(field_name="results"))
