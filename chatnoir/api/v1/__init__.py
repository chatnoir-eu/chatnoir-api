from typing import List, Tuple
from typing import Set

from requests import Response, post

from chatnoir.api.util import LazyResults
from chatnoir.api.v1.constants import API_URL
from chatnoir.api.v1.model import (
    SearchResponse, SearchRequest, ResponseMeta, SearchResponseResult
)
from chatnoir.constants import DEFAULT_INDICES
from chatnoir.model.index import Index
from chatnoir.model.result import (
    SearchResults, SearchResult, ResultsMeta, PhraseSearchResults,
    PhraseSearchResult, MinimalPhraseSearchResults, MinimalPhraseSearchResult
)


def search(
        api_key: str,
        query: str,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
) -> SearchResults:
    return LazySearchResults(api_key, query, index, explain, 10)


class LazySearchResults(
    SearchResults,
    LazyResults[SearchResult, SearchResults]
):
    _api_key: str
    _query: str
    _index: Set[Index]
    _explain: bool

    def __init__(
            self,
            api_key: str,
            query: str,
            index: Set[Index],
            explain: bool,
            size: int,
    ):
        super(LazySearchResults, self).__init__(size)
        self._api_key = api_key
        self._query = query
        self._index = index
        self._explain = explain

    def page(
            self,
            start: int,
            size: int
    ) -> Tuple[ResultsMeta, List[SearchResult]]:
        return search_page(
            self._api_key,
            self._query,
            start, size,
            self._index,
            self._explain
        )


def search_page(
        api_key: str,
        query: str,
        start: int,
        size: int,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
) -> Tuple[ResultsMeta, List[SearchResult]]:
    request = SearchRequest(
        apikey=api_key,
        query=query,
        start=start,
        size=size,
        index=index,
        explain=explain,
    )
    request_json = request.to_json()

    headers = {
        "Accept": "application/json",
        "Content-Type": "text/plain",
    }
    raw_response: Response = post(
        f"{API_URL}/_search",
        headers=headers,
        data=request_json.encode("utf-8")
    )

    response_json = raw_response.text
    response = SearchResponse.from_json(response_json)

    return response.meta, response.results


def search_phrases(
        api_key: str,
        query: str,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
) -> PhraseSearchResults:
    raise NotImplementedError()


def search_phrases_page(
        api_key: str,
        query: str,
        start: int,
        size: int,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
) -> Tuple[ResultsMeta, List[PhraseSearchResult]]:
    raise NotImplementedError()


def search_phrases_minimal(
        api_key: str,
        query: str,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
) -> MinimalPhraseSearchResults:
    raise NotImplementedError()


def search_phrases_minimal_page(
        api_key: str,
        query: str,
        start: int,
        size: int,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
) -> Tuple[ResultsMeta, List[MinimalPhraseSearchResult]]:
    raise NotImplementedError()
