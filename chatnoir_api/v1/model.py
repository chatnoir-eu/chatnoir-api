from datetime import datetime
from typing import Optional, Sequence, AbstractSet
from uuid import UUID

from pydantic import BaseModel, Field, PlainSerializer, PlainValidator
from typing_extensions import Annotated

from chatnoir_api.model import (
    Index,
    Slop,
    index_id,
    parse_index,
    SearchMethod,
    decode_uuid,
)
from chatnoir_api.model.highlight import HighlightedText
from chatnoir_api.model.result import (
    Meta,
    Result,
    MinimalResult,
    ExplainedMinimalResult,
    Explanation,
    ExplainedResult,
    Results,
    ResultsMixin,
)


class Request(BaseModel, frozen=True):
    apikey: str
    query: str
    index: Annotated[
        AbstractSet[Index],
        PlainSerializer(lambda indices: {index_id(index) for index in indices}),
    ]
    start: Annotated[
        Optional[int],
        Field(serialization_alias="from"),
    ]
    size: Optional[int] = None
    explain: bool
    minimal: bool
    search_method: SearchMethod


class PhraseRequest(Request, BaseModel, frozen=True):
    slop: Optional[Slop]


class MinimalResultResponse(MinimalResult, BaseModel, frozen=True):
    score: float
    uuid: Annotated[UUID, PlainValidator(decode_uuid)]
    target_uri: Optional[str] = None
    snippet: Annotated[HighlightedText, PlainValidator(HighlightedText)]
    index: Annotated[Index, PlainValidator(parse_index)]
    title: Annotated[HighlightedText, PlainValidator(HighlightedText)]


class ExplanationResponse(Explanation, BaseModel, frozen=True):
    value: float
    description: str
    details: Sequence["ExplanationResponse"]  # type: ignore[override]


class ExplainedMinimalResultResponse(
    MinimalResultResponse, ExplainedMinimalResult, BaseModel, frozen=True
):
    explanation: ExplanationResponse  # type: ignore[override]


class ResultResponse(MinimalResultResponse, Result, BaseModel, frozen=True):
    index: Annotated[
        Index,
        PlainValidator(parse_index),
    ]
    trec_id: Optional[str]
    target_hostname: Optional[str]
    page_rank: Optional[float]
    spam_rank: Optional[float]
    title: Annotated[
        HighlightedText,
        PlainValidator(HighlightedText),
    ]
    warc_id: Optional[str]
    cache_uri: str
    crawl_date: Optional[datetime]
    content_type: Optional[str]
    language: Annotated[
        str,
        Field(validation_alias="lang"),
    ]


class ExplainedResultResponse(
    ResultResponse,
    ExplainedMinimalResultResponse,
    ExplainedResult,
    BaseModel,
    frozen=True,
):
    explanation: ExplanationResponse  # type: ignore[override]


class MetaResponse(Meta, BaseModel, frozen=True):
    indices: Annotated[
        AbstractSet[Index], PlainValidator(lambda ids: {parse_index(id) for id in ids})
    ]
    query_time: int
    total_results: int
    search_method: SearchMethod


class MinimalSearchResponse(  # type: ignore
    ResultsMixin[MetaResponse, MinimalResultResponse],
    BaseModel,
    Results[MetaResponse, MinimalResultResponse],
    frozen=True,
):
    meta: MetaResponse
    results: Sequence[MinimalResultResponse]


class ExplainedMinimalSearchResponse(  # type: ignore
    ResultsMixin[MetaResponse, MinimalResultResponse],
    BaseModel,
    Results[MetaResponse, MinimalResultResponse],
    frozen=True,
):
    meta: MetaResponse
    results: Sequence[ExplainedMinimalResultResponse]  # type: ignore[override]


class SearchResponse(  # type: ignore
    ResultsMixin[MetaResponse, MinimalResultResponse],
    BaseModel,
    Results[MetaResponse, MinimalResultResponse],
    frozen=True,
):
    meta: MetaResponse
    results: Sequence[ResultResponse]  # type: ignore[override]


class ExplainedSearchResponse(  # type: ignore
    ResultsMixin[MetaResponse, MinimalResultResponse],
    BaseModel,
    Results[MetaResponse, MinimalResultResponse],
    frozen=True,
):
    meta: MetaResponse
    results: Sequence[ExplainedResultResponse]  # type: ignore[override]
