from typing import List, Tuple, Type, overload, Union, Set

from chatnoir_api.lazy import LazyResultSequence
from chatnoir_api.model import Index, Slop
from chatnoir_api.model.result import (
    ResultsMeta, PhraseSearchResult, MinimalPhraseSearchResult, Results
)
from chatnoir_api.types import Literal
from chatnoir_api.v1.defaults import (
    DEFAULT_START, DEFAULT_SIZE, DEFAULT_SLOP, DEFAULT_INDEX, DEFAULT_MINIMAL,
    DEFAULT_EXPLAIN, DEFAULT_RETRIES, DEFAULT_BACKOFF_SECONDS
)
from chatnoir_api.v1.model import (
    PhraseSearchRequest, PhraseSearchResponse, MinimalPhraseSearchResponse
)
from chatnoir_api.v1.requests import request_page


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
) -> Results[PhraseSearchResult]:
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
) -> Results[MinimalPhraseSearchResult]:
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
) -> Results[Union[PhraseSearchResult, MinimalPhraseSearchResult]]:
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
) -> Results[Union[PhraseSearchResult, MinimalPhraseSearchResult]]:
    def load_page(
            start: int,
            size: int
    ) -> Tuple[
        ResultsMeta,
        List[Union[MinimalPhraseSearchResult, PhraseSearchResult]]
    ]:
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

    return LazyResultSequence(
        page_size,
        load_page,
    )


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
    response = request_page(
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
