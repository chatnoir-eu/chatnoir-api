from typing import List, Tuple, TypeVar, Type
from typing import Set

from dataclasses_json import DataClassJsonMixin
from requests import Response as RResponse, post

from chatnoir.api.util import LazyResults
from chatnoir.api.v1.constants import API_URL
from chatnoir.api.v1.model import (
    SearchResponse, SearchRequest, ResponseMeta, SearchResponseResult, Request,
    Response, MinimalPhraseSearchResponse, MinimalPhraseSearchRequest,
    PhraseSearchRequest, PhraseSearchResponse
)
from chatnoir.constants import DEFAULT_INDICES
from chatnoir.model import Index, Slop
from chatnoir.model.result import (
    SearchResults, SearchResult, ResultsMeta, PhraseSearchResults,
    PhraseSearchResult, MinimalPhraseSearchResults, MinimalPhraseSearchResult
)

_JsonRequest = TypeVar("_JsonRequest", Request, DataClassJsonMixin)
_JsonResponse = TypeVar("_JsonResponse", Response, DataClassJsonMixin)


def _request_page(
        request: _JsonRequest,
        response_type: Type[_JsonResponse],
        endpoint: str,
) -> _JsonResponse:
    request_json = request.to_json()

    headers = {
        "Accept": "application/json",
        "Content-Type": "text/plain",
    }
    raw_response: RResponse = post(
        f"{API_URL}/{endpoint}",
        headers=headers,
        data=request_json.encode("utf-8")
    )

    response_json = raw_response.text
    response = response_type.from_json(response_json)

    return response


def search(
        api_key: str,
        query: str,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
        page_size: int = 100,
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


def search_phrases(
        api_key: str,
        query: str,
        slop: Slop = 0,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
        page_size: int = 100,
) -> PhraseSearchResults:
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
                explain
            )

    return LazyPhraseSearchResults(page_size)


def search_phrases_page(
        api_key: str,
        query: str,
        start: int,
        size: int,
        slop: Slop = 0,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
) -> Tuple[ResultsMeta, List[PhraseSearchResult]]:
    response = _request_page(
        PhraseSearchRequest(
            apikey=api_key,
            query=query,
            start=start,
            size=size,
            index=index,
            explain=explain,
            slop=slop,
        ),
        PhraseSearchResponse,
        "_phrases"
    )
    return response.meta, response.results


def search_phrases_minimal(
        api_key: str,
        query: str,
        slop: Slop = 0,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
        page_size: int = 100,
) -> MinimalPhraseSearchResults:
    class LazyMinimalPhraseSearchResults(
        MinimalPhraseSearchResults,
        LazyResults[MinimalPhraseSearchResult]
    ):
        def page(
                self,
                start: int,
                size: int
        ) -> Tuple[ResultsMeta, List[MinimalPhraseSearchResult]]:
            return search_phrases_minimal_page(
                api_key,
                query,
                start,
                size,
                slop,
                index,
                explain
            )

    return LazyMinimalPhraseSearchResults(page_size)


def search_phrases_minimal_page(
        api_key: str,
        query: str,
        start: int,
        size: int,
        slop: Slop = 0,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
) -> Tuple[ResultsMeta, List[MinimalPhraseSearchResult]]:
    response = _request_page(
        MinimalPhraseSearchRequest(
            apikey=api_key,
            query=query,
            start=start,
            size=size,
            index=index,
            explain=explain,
            slop=slop,
        ),
        MinimalPhraseSearchResponse,
        "_phrases"
    )
    return response.meta, response.results
