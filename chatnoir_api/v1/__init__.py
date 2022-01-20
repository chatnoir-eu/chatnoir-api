from random import uniform
from time import sleep
from typing import List, Tuple, TypeVar, Type, overload, Union, Set

from dataclasses_json import DataClassJsonMixin
from requests import Response as HttpResponse, post

from chatnoir_api import logger
from chatnoir_api.constants import API_V1_URL
from chatnoir_api.util import LazyResults
from chatnoir_api.v1.defaults import (
    DEFAULT_START, DEFAULT_SIZE, DEFAULT_SLOP, DEFAULT_INDEX, DEFAULT_MINIMAL,
    DEFAULT_EXPLAIN, DEFAULT_RETRIES, DEFAULT_BACKOFF_SECONDS
)
from chatnoir_api.v1.model import (
    SearchResponse, SearchRequest, Request, Response, PhraseSearchRequest,
    PhraseSearchResponse, MinimalPhraseSearchResponse
)
from chatnoir_api.model import Index, Slop
from chatnoir_api.model.result import (
    ResultsMeta, SearchResults, SearchResult, PhraseSearchResults,
    PhraseSearchResult, MinimalPhraseSearchResults, MinimalPhraseSearchResult
)
from chatnoir_api.types import Literal

_JsonRequest = TypeVar("_JsonRequest", Request, DataClassJsonMixin)
_JsonResponse = TypeVar("_JsonResponse", Response, DataClassJsonMixin)


def _request_page(
        request: _JsonRequest,
        response_type: Type[_JsonResponse],
        endpoint: str,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> _JsonResponse:
    request_json = request.to_json()

    headers = {
        "Accept": "application/json",
        "Content-Type": "text/plain",
    }
    raw_response: HttpResponse = post(
        f"{API_V1_URL}/{endpoint}",
        headers=headers,
        data=request_json.encode("utf-8")
    )
    if raw_response.status_code // 100 == 5:
        if retries == 0:
            raise RuntimeError(
                "ChatNoir API internal server error. "
                "Please get in contact with the admins "
                "at https://chatnoir.eu/doc/"
            )
        else:
            logger.warning(
                f"ChatNoir API internal server error. "
                f"Retrying in {round(backoff_seconds)} seconds."
            )
            sleep(backoff_seconds)
            return _request_page(
                request,
                response_type,
                endpoint,
                retries - 1,
                round(backoff_seconds) * 2 + uniform(-0.5, 0.5)
            )
    if raw_response.status_code == 401:
        raise RuntimeError(
            "ChatNoir API key invalid or missing. "
            "Please refer to the documentation at https://chatnoir.eu/doc/api/"
        )
    elif raw_response.status_code == 403:
        raise RuntimeError(
            "ChatNoir API blocked this IP address. "
            "Please get in contact with the admins at https://chatnoir.eu/doc/"
        )
    elif raw_response.status_code == 429:
        if retries == 0:
            raise RuntimeError(
                "ChatNoir API quota exceeded. Please throttle requests and "
                "refer to the documentation at https://chatnoir.eu/doc/api/"
            )
        else:
            logger.warning(
                f"ChatNoir API quota exceeded. "
                f"Retrying in {round(backoff_seconds)} seconds."
            )
        sleep(backoff_seconds)
        return _request_page(
            request,
            response_type,
            endpoint,
            retries - 1,
            round(backoff_seconds) * 2 + uniform(-0.5, 0.5)
        )
    elif not raw_response.ok:
        raise RuntimeError(
            f"ChatNoir API request failed "
            f"with code {raw_response.status_code}."
            f"Please refer to the documentation at https://chatnoir.eu/doc/ "
            f"or get in contact with the admins."
        )

    response_json = raw_response.text
    response = response_type.from_json(response_json)

    return response


def search(
        api_key: str,
        query: str,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        explain: bool = DEFAULT_EXPLAIN,
        page_size: int = DEFAULT_SIZE,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> SearchResults:
    class LazySearchResults(SearchResults, LazyResults[SearchResult]):
        def page(
                self,
                start: int,
                size: int
        ) -> Tuple[ResultsMeta, List[SearchResult]]:
            return search_page(
                api_key=api_key,
                query=query,
                start=start,
                size=size,
                index=index,
                explain=explain,
                retries=retries,
                backoff_seconds=backoff_seconds,
            )

    return LazySearchResults(page_size)


def search_page(
        api_key: str,
        query: str,
        start: int = DEFAULT_START,
        size: int = DEFAULT_SIZE,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        explain: bool = DEFAULT_EXPLAIN,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> Tuple[ResultsMeta, List[SearchResult]]:
    if isinstance(index, Index):
        index = {index}
    index: Set[Index]

    response = _request_page(
        request=SearchRequest(
            apikey=api_key,
            query=query,
            start=start,
            size=size,
            index=index,
            explain=explain,
        ),
        response_type=SearchResponse,
        endpoint="_search",
        retries=retries,
        backoff_seconds=backoff_seconds,
    )
    return response.meta, response.results


@overload
def search_phrases(
        api_key: str,
        query: str,
        slop: Slop = DEFAULT_SLOP,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        minimal: Literal[False] = DEFAULT_MINIMAL,
        explain: bool = DEFAULT_EXPLAIN,
        page_size: int = DEFAULT_SIZE,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> PhraseSearchResults:
    pass


@overload
def search_phrases(
        api_key: str,
        query: str,
        slop: Slop = DEFAULT_SLOP,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        minimal: Literal[True] = DEFAULT_MINIMAL,
        explain: bool = DEFAULT_EXPLAIN,
        page_size: int = DEFAULT_SIZE,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> MinimalPhraseSearchResults:
    pass


@overload
def search_phrases(
        api_key: str,
        query: str,
        slop: Slop = DEFAULT_SLOP,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        minimal: bool = DEFAULT_MINIMAL,
        explain: bool = DEFAULT_EXPLAIN,
        page_size: int = DEFAULT_SIZE,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> Union[PhraseSearchResults, MinimalPhraseSearchResults]:
    pass


def search_phrases(
        api_key: str,
        query: str,
        slop: Slop = DEFAULT_SLOP,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        minimal: bool = DEFAULT_MINIMAL,
        explain: bool = DEFAULT_EXPLAIN,
        page_size: int = DEFAULT_SIZE,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> Union[PhraseSearchResults, MinimalPhraseSearchResults]:
    results_type: Type[Union[MinimalPhraseSearchResults, PhraseSearchResults]]
    result_type: Type[Union[MinimalPhraseSearchResult, PhraseSearchResult]]
    if minimal:
        results_type = MinimalPhraseSearchResults
        result_type = MinimalPhraseSearchResult
    else:
        results_type = PhraseSearchResults
        result_type = PhraseSearchResult

    class LazyPhraseSearchResults(
        results_type,
        LazyResults[result_type]
    ):
        def page(
                self,
                start: int,
                size: int
        ) -> Tuple[ResultsMeta, List[result_type]]:
            return search_phrases_page(
                api_key=api_key,
                query=query,
                start=start,
                size=size,
                slop=slop,
                index=index,
                minimal=minimal,
                explain=explain,
                retries=retries,
                backoff_seconds=backoff_seconds,
            )

    return LazyPhraseSearchResults(page_size)


@overload
def search_phrases_page(
        api_key: str,
        query: str,
        start: int = DEFAULT_START,
        size: int = DEFAULT_SIZE,
        slop: Slop = DEFAULT_SLOP,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        minimal: Literal[False] = DEFAULT_MINIMAL,
        explain: bool = DEFAULT_EXPLAIN,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> Tuple[ResultsMeta, List[PhraseSearchResult]]:
    pass


@overload
def search_phrases_page(
        api_key: str,
        query: str,
        start: int = DEFAULT_START,
        size: int = DEFAULT_SIZE,
        slop: Slop = DEFAULT_SLOP,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        minimal: Literal[True] = DEFAULT_MINIMAL,
        explain: bool = DEFAULT_EXPLAIN,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> Tuple[ResultsMeta, List[MinimalPhraseSearchResult]]:
    pass


@overload
def search_phrases_page(
        api_key: str,
        query: str,
        start: int = DEFAULT_START,
        size: int = DEFAULT_SIZE,
        slop: Slop = DEFAULT_SLOP,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        minimal: bool = DEFAULT_MINIMAL,
        explain: bool = DEFAULT_EXPLAIN,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> Tuple[
    ResultsMeta,
    List[Union[PhraseSearchResult, MinimalPhraseSearchResult]]
]:
    pass


def search_phrases_page(
        api_key: str,
        query: str,
        start: int = DEFAULT_START,
        size: int = DEFAULT_SIZE,
        slop: Slop = DEFAULT_SLOP,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        minimal: bool = DEFAULT_MINIMAL,
        explain: bool = DEFAULT_EXPLAIN,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> Tuple[
    ResultsMeta,
    List[Union[PhraseSearchResult, MinimalPhraseSearchResult]]
]:
    if isinstance(index, Index):
        index = {index}
    index: Set[Index]

    response_type: Type[
        Union[MinimalPhraseSearchResponse, PhraseSearchResponse]
    ]
    if minimal:
        response_type = MinimalPhraseSearchResponse
    else:
        response_type = PhraseSearchResponse
    response = _request_page(
        request=PhraseSearchRequest(
            apikey=api_key,
            query=query,
            start=start,
            size=size,
            index=index,
            explain=explain,
            minimal=minimal,
            slop=slop,
        ),
        response_type=response_type,
        endpoint="_phrases",
        retries=retries,
        backoff_seconds=backoff_seconds,
    )
    return response.meta, response.results
