from typing import Type, Union, Set

from chatnoir_api.lazy import LazyResultSequence
from chatnoir_api.model import Index
from chatnoir_api.model.result import (
    MinimalResult, ExplainedMinimalResult, Result, ExplainedResult,
    Meta, ExtendedMeta, Results, MinimalResultStaging,
    ExplainedMinimalResultStaging, ResultStaging, ExplainedResultStaging
)
from chatnoir_api.v1.defaults import (
    DEFAULT_START, DEFAULT_SIZE, DEFAULT_INDEX, DEFAULT_MINIMAL,
    DEFAULT_EXPLAIN, DEFAULT_RETRIES, DEFAULT_BACKOFF_SECONDS,
    DEFAULT_EXTENDED_META, DEFAULT_STAGING
)
from chatnoir_api.v1.model import (
    MinimalResponse, ExplainedMinimalResponse,
    Response, ExplainedResponse,
    MinimalResponseStaging, ExplainedMinimalResponseStaging,
    ResponseStaging, ExplainedResponseStaging,
    ExtendedMetaMinimalResponseStaging,
    ExplainedExtendedMetaMinimalResponseStaging,
    ExtendedMetaResponseStaging, ExplainedExtendedMetaResponseStaging,
    Request, RequestStaging
)
from chatnoir_api.v1.requests import request_page


def search(
        api_key: str,
        query: str,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        minimal: bool = DEFAULT_MINIMAL,
        explain: bool = DEFAULT_EXPLAIN,
        extended_meta: bool = DEFAULT_EXTENDED_META,
        staging: bool = DEFAULT_STAGING,
        page_size: int = DEFAULT_SIZE,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> Results[
    Union[Meta, ExtendedMeta],
    Union[
        MinimalResult, ExplainedMinimalResult,
        Result, ExplainedResult,
        MinimalResultStaging, ExplainedMinimalResultStaging,
        ResultStaging, ExplainedResultStaging,
    ]
]:
    def load_page(
            start: int,
            size: int
    ) -> Results[
        Union[Meta, ExtendedMeta],
        Union[
            MinimalResult, ExplainedMinimalResult,
            Result, ExplainedResult,
            MinimalResultStaging, ExplainedMinimalResultStaging,
            ResultStaging, ExplainedResultStaging,
        ]
    ]:
        return search_page(
            api_key=api_key,
            query=query,
            index=index,
            minimal=minimal,
            explain=explain,
            extended_meta=extended_meta,
            staging=staging,
            start=start,
            size=size,
            retries=retries,
            backoff_seconds=backoff_seconds,
        )

    return LazyResultSequence(
        page_size,
        load_page,
    )


def search_page(
        api_key: str,
        query: str,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        minimal: bool = DEFAULT_MINIMAL,
        explain: bool = DEFAULT_EXPLAIN,
        extended_meta: bool = DEFAULT_EXTENDED_META,
        staging: bool = DEFAULT_STAGING,
        start: int = DEFAULT_START,
        size: int = DEFAULT_SIZE,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> Results[
    Union[Meta, ExtendedMeta],
    Union[
        MinimalResult, ExplainedMinimalResult,
        Result, ExplainedResult,
        MinimalResultStaging, ExplainedMinimalResultStaging,
        ResultStaging, ExplainedResultStaging,
    ]
]:
    if isinstance(index, Index):
        index = {index}
    index: Set[Index]

    request: Union[Request, RequestStaging]
    response_type: Type[Union[
        MinimalResponse, ExplainedMinimalResponse,
        Response, ExplainedResponse,
        MinimalResponseStaging, ExplainedMinimalResponseStaging,
        ResponseStaging, ExplainedResponseStaging,
        ExtendedMetaMinimalResponseStaging,
        ExplainedExtendedMetaMinimalResponseStaging,
        ExtendedMetaResponseStaging, ExplainedExtendedMetaResponseStaging
    ]]
    if not staging:
        request = Request(
            apikey=api_key,
            query=query,
            start=start,
            size=size,
            index=index,
            explain=explain,
            minimal=minimal,
        )
        if extended_meta:
            raise ValueError(
                "Extended meta is not supported on the legacy API."
            )
        if minimal:
            raise ValueError(
                "Minimal response is not supported on the legacy API."
            )
        if not explain:
            response_type = Response
        else:
            response_type = ExplainedResponse
    else:
        request = RequestStaging(
            apikey=api_key,
            query=query,
            start=start,
            size=size,
            index=index,
            explain=explain,
            minimal=minimal,
            extended_meta=extended_meta,
        )
        if not extended_meta:
            if minimal:
                if not explain:
                    response_type = MinimalResponseStaging
                else:
                    response_type = ExplainedMinimalResponseStaging
            else:
                if not explain:
                    response_type = ResponseStaging
                else:
                    response_type = ExplainedResponseStaging
        else:
            if minimal:
                if not explain:
                    response_type = ExtendedMetaMinimalResponseStaging
                else:
                    response_type = ExplainedExtendedMetaMinimalResponseStaging
            else:
                if not explain:
                    response_type = ExtendedMetaResponseStaging
                else:
                    response_type = ExplainedExtendedMetaResponseStaging

    response = request_page(
        request=request,
        response_type=response_type,
        endpoint="_search",
        retries=retries,
        backoff_seconds=backoff_seconds,
        staging=staging,
    )
    return response
