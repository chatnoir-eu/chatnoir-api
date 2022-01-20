from random import uniform
from time import sleep
from typing import List, Tuple, TypeVar, Type, overload, Union, Set

from dataclasses_json import DataClassJsonMixin
from requests import Response as HttpResponse, post

from chatnoir_api import logger
from chatnoir_api.constants import DEFAULT_INDICES
from chatnoir_api.util import LazyResults
from chatnoir_api.v1.constants import API_URL
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
        retries: int = 5,
        backoff_seconds: float = 1 + uniform(-0.5, 0.5),
) -> _JsonResponse:
    request_json = request.to_json()

    headers = {
        "Accept": "application/json",
        "Content-Type": "text/plain",
    }
    raw_response: HttpResponse = post(
        f"{API_URL}/{endpoint}",
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
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
        page_size: int = 10,
) -> SearchResults:
    class LazySearchResults(SearchResults, LazyResults[SearchResult]):
        def page(
                self,
                start: int,
                size: int
        ) -> Tuple[ResultsMeta, List[SearchResult]]:
            return search_page(
                api_key,
                query,
                start,
                size,
                index,
                explain
            )

    return LazySearchResults(page_size)


def search_page(
        api_key: str,
        query: str,
        start: int,
        size: int,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
) -> Tuple[ResultsMeta, List[SearchResult]]:
    response = _request_page(
        SearchRequest(
            apikey=api_key,
            query=query,
            start=start,
            size=size,
            index=index,
            explain=explain,
        ),
        SearchResponse,
        "_search"
    )
    return response.meta, response.results


@overload
def search_phrases(
        api_key: str,
        query: str,
        slop: Slop = 0,
        index: Set[Index] = DEFAULT_INDICES,
        minimal: Literal[False] = False,
        explain: bool = False,
        page_size: int = 10,
) -> PhraseSearchResults:
    pass


@overload
def search_phrases(
        api_key: str,
        query: str,
        slop: Slop = 0,
        index: Set[Index] = DEFAULT_INDICES,
        minimal: Literal[True] = False,
        explain: bool = False,
        page_size: int = 10,
) -> MinimalPhraseSearchResults:
    pass


def search_phrases(
        api_key: str,
        query: str,
        slop: Slop = 0,
        index: Set[Index] = DEFAULT_INDICES,
        minimal: bool = False,
        explain: bool = False,
        page_size: int = 10,
) -> Union[PhraseSearchResults, MinimalPhraseSearchResults]:
    if minimal:
        class LazyPhraseSearchResults(
            PhraseSearchResults,
            LazyResults[PhraseSearchResult]
        ):
            def page(
                    self,
                    start: int,
                    size: int
            ) -> Tuple[ResultsMeta, List[PhraseSearchResult]]:
                return search_phrases_page(
                    api_key,
                    query,
                    start,
                    size,
                    slop,
                    index,
                    False,
                    explain,
                )
    else:
        class LazyPhraseSearchResults(
            MinimalPhraseSearchResults,
            LazyResults[MinimalPhraseSearchResult]
        ):
            def page(
                    self,
                    start: int,
                    size: int
            ) -> Tuple[ResultsMeta, List[MinimalPhraseSearchResult]]:
                return search_phrases_page(
                    api_key,
                    query,
                    start,
                    size,
                    slop,
                    index,
                    False,
                    explain,
                )

    return LazyPhraseSearchResults(page_size)


@overload
def search_phrases_page(
        api_key: str,
        query: str,
        start: int,
        size: int,
        slop: Slop = 0,
        index: Set[Index] = DEFAULT_INDICES,
        minimal: Literal[False] = False,
        explain: bool = False,
) -> Tuple[ResultsMeta, List[PhraseSearchResult]]:
    pass


@overload
def search_phrases_page(
        api_key: str,
        query: str,
        start: int,
        size: int,
        slop: Slop = 0,
        index: Set[Index] = DEFAULT_INDICES,
        minimal: Literal[True] = False,
        explain: bool = False,
) -> Tuple[ResultsMeta, List[MinimalPhraseSearchResult]]:
    pass


def search_phrases_page(
        api_key: str,
        query: str,
        start: int,
        size: int,
        slop: Slop = 0,
        index: Set[Index] = DEFAULT_INDICES,
        minimal: bool = False,
        explain: bool = False,
) -> Union[
    Tuple[ResultsMeta, List[PhraseSearchResult]],
    Tuple[ResultsMeta, List[MinimalPhraseSearchResult]]
]:
    response = _request_page(
        PhraseSearchRequest(
            apikey=api_key,
            query=query,
            start=start,
            size=size,
            index=index,
            explain=explain,
            minimal=minimal,
            slop=slop,
        ),
        MinimalPhraseSearchResponse if minimal else PhraseSearchResponse,
        "_phrases"
    )
    return response.meta, response.results
