from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Set
from uuid import UUID

from dataclasses_json import config, DataClassJsonMixin

from chatnoir_api.model import Index, Slop, decode_uuid
from chatnoir_api.model.highlight import HighlightedText
from chatnoir_api.model.result import Meta, Result, ExtendedMeta, MetaIndex, \
    MinimalResult, MinimalResultStaging, ExplainedMinimalResult, Explanation, \
    ExplainedMinimalResultStaging, ExplainedResult, ResultStaging, \
    ExplainedResultStaging, ResultsMixin


@dataclass(frozen=True)
class Request(DataClassJsonMixin):
    apikey: str
    query: str
    index: Set[Index] = field(metadata=config(
        encoder=lambda indices: {index.value for index in indices}
    ))
    start: Optional[int] = field(metadata=config(
        field_name="from"
    ))
    size: Optional[int]
    explain: bool
    minimal: bool


@dataclass(frozen=True)
class PhraseRequest(Request, DataClassJsonMixin, ABC):
    slop: Optional[Slop]


@dataclass(frozen=True)
class RequestStaging(Request, DataClassJsonMixin, ABC):
    extended_meta: bool


@dataclass(frozen=True)
class PhraseRequestStaging(
    RequestStaging, DataClassJsonMixin, ABC
):
    slop: Optional[Slop]


@dataclass(frozen=True)
class MinimalResultResponse(MinimalResult, DataClassJsonMixin):
    score: float
    uuid: UUID = field(metadata=config(
        decoder=decode_uuid
    ))
    target_uri: str
    snippet: HighlightedText = field(metadata=config(
        decoder=HighlightedText
    ))


@dataclass(frozen=True)
class ExplanationResponse(Explanation, DataClassJsonMixin):
    value: float
    description: str
    details: List["Explanation"]


@dataclass(frozen=True)
class ExplainedMinimalResultResponse(
    MinimalResultResponse, ExplainedMinimalResult, DataClassJsonMixin
):
    explanation: ExplanationResponse


@dataclass(frozen=True)
class ResultResponse(MinimalResultResponse, Result, DataClassJsonMixin):
    index: Index = field(metadata=config(
        encoder=str,
        decoder=Index
    ))
    trec_id: Optional[str]
    target_hostname: str
    page_rank: Optional[float]
    spam_rank: Optional[float]
    title: HighlightedText = field(metadata=config(
        encoder=str,
        decoder=HighlightedText
    ))


@dataclass(frozen=True)
class ExplainedResultResponse(
    ResultResponse, ExplainedResult, DataClassJsonMixin
):
    explanation: ExplanationResponse


@dataclass(frozen=True)
class MinimalResultResponseStaging(
    MinimalResultResponse, MinimalResultStaging, DataClassJsonMixin
):
    index: Index = field(metadata=config(
        decoder=Index
    ))
    title: HighlightedText = field(metadata=config(
        encoder=str,
        decoder=HighlightedText,
    ))


@dataclass(frozen=True)
class ExplainedMinimalResultResponseStaging(
    ExplainedMinimalResultResponse, ExplainedMinimalResultStaging,
    DataClassJsonMixin
):
    explanation: ExplanationResponse


@dataclass(frozen=True)
class ResultResponseStaging(
    ResultResponse, ResultStaging, DataClassJsonMixin
):
    warc_id: Optional[str]
    cache_uri: Optional[str]
    crawl_date: Optional[datetime]
    content_type: str
    language: str = field(metadata=config(field_name="lang"))


@dataclass(frozen=True)
class ExplainedResultResponseStaging(
    ExplainedResultResponse, ExplainedResultStaging, DataClassJsonMixin
):
    explanation: ExplanationResponse


@dataclass(frozen=True)
class MetaResponse(Meta, DataClassJsonMixin):
    indices: Set[Index] = field(metadata=config(
        decoder=lambda indices: {Index(index) for index in indices}
    ))
    query_time: int
    total_results: int


@dataclass(frozen=True)
class MetaIndexResponse(MetaIndex, DataClassJsonMixin):
    index: Index = field(metadata=config(
        decoder=Index,
        field_name="id",
    ))
    name: str
    selected: bool


@dataclass(frozen=True)
class ExtendedMetaResponse(MetaResponse, ExtendedMeta, DataClassJsonMixin):
    indices: Set[MetaIndexResponse]
    explain: bool
    max_page: int
    page_size: int
    query_string: str
    results_from: int
    results_to: int
    terminated_early: bool


@dataclass(frozen=True)
class MinimalResponse(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: MetaResponse
    results: List[MinimalResultResponse]


@dataclass(frozen=True)
class ExplainedMinimalResponse(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: MetaResponse
    results: List[ExplainedMinimalResultResponse]


@dataclass(frozen=True)
class Response(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: MetaResponse
    results: List[ResultResponse]


@dataclass(frozen=True)
class ExplainedResponse(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: MetaResponse
    results: List[ExplainedResultResponse]


@dataclass(frozen=True)
class MinimalResponseStaging(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: MetaResponse
    results: List[MinimalResultResponseStaging]


@dataclass(frozen=True)
class ExplainedMinimalResponseStaging(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]

):
    meta: MetaResponse
    results: List[ExplainedMinimalResultResponseStaging]


@dataclass(frozen=True)
class ResponseStaging(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: MetaResponse
    results: List[ResultResponseStaging]


@dataclass(frozen=True)
class ExplainedResponseStaging(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: MetaResponse
    results: List[ExplainedResultResponseStaging]


@dataclass(frozen=True)
class ExtendedMetaMinimalResponseStaging(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: ExtendedMetaResponse
    results: List[MinimalResultResponseStaging]


@dataclass(frozen=True)
class ExplainedExtendedMetaMinimalResponseStaging(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: ExtendedMetaResponse
    results: List[ExplainedMinimalResultResponseStaging]


@dataclass(frozen=True)
class ExtendedMetaResponseStaging(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: ExtendedMetaResponse
    results: List[ResultResponseStaging]


@dataclass(frozen=True)
class ExplainedExtendedMetaResponseStaging(
    DataClassJsonMixin,
    ResultsMixin[MetaResponse, MinimalResultResponse]
):
    meta: ExtendedMetaResponse
    results: List[ExplainedResultResponseStaging]
