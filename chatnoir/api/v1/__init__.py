from typing import List, Tuple
from typing import Set

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
    raise NotImplementedError()


def search_page(
        api_key: str,
        query: str,
        start: int,
        size: int,
        index: Set[Index] = DEFAULT_INDICES,
        explain: bool = False,
) -> Tuple[ResultsMeta, List[SearchResult]]:
    raise NotImplementedError()


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
