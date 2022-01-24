from typing import List, Tuple, Union, Set

from chatnoir_api.lazy import LazyResultSequence
from chatnoir_api.model import Index
from chatnoir_api.model.result import ResultsMeta, SearchResult, Results
from chatnoir_api.v1.defaults import (
    DEFAULT_START, DEFAULT_SIZE, DEFAULT_INDEX, DEFAULT_EXPLAIN,
    DEFAULT_RETRIES, DEFAULT_BACKOFF_SECONDS
)
from chatnoir_api.v1.model import SearchResponse, SearchRequest
from chatnoir_api.v1.requests import request_page


def search(
        api_key: str,
        query: str,
        index: Union[Index, Set[Index]] = DEFAULT_INDEX,
        explain: bool = DEFAULT_EXPLAIN,
        page_size: int = DEFAULT_SIZE,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> Results[SearchResult]:
    def load_page(
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

    return LazyResultSequence(
        page_size,
        load_page,
    )


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

    response = request_page(
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
