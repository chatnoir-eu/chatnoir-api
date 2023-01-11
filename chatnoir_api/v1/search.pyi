from typing import Union, Set, overload, Literal

from chatnoir_api.model import Index
from chatnoir_api.model.result import Meta, MinimalResult, Result, \
    ExplainedResult, ExplainedMinimalResult, ExtendedMeta, Results, \
    MinimalResultStaging, ExplainedMinimalResultStaging, ResultStaging, \
    ExplainedResultStaging


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[False] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[Meta, Result]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[True] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[Meta, ResultStaging]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[False] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[ExtendedMeta, Result]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[True] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[ExtendedMeta, ResultStaging]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[False] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[Meta, ExplainedResult]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[True] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[Meta, ExplainedResultStaging]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[False] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[ExtendedMeta, ExplainedResult]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[True] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[ExtendedMeta, ExplainedResultStaging]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[False] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[Meta, MinimalResult]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[True] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[Meta, MinimalResultStaging]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[False] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[ExtendedMeta, MinimalResult]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[True] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[ExtendedMeta, MinimalResultStaging]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[False] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[Meta, ExplainedMinimalResult]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[True] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[Meta, ExplainedMinimalResultStaging]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[False] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[ExtendedMeta, ExplainedMinimalResult]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[True] = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[ExtendedMeta, ExplainedMinimalResultStaging]: ...


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: bool = ..., explain: bool = ...,
        extended_meta: bool = ..., staging: bool = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[
    Union[Meta, ExtendedMeta],
    Union[
        MinimalResult, ExplainedMinimalResult,
        Result, ExplainedResult,
        MinimalResultStaging, ExplainedMinimalResultStaging,
        ResultStaging, ExplainedResultStaging,
    ]
]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[False] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[Meta, Result]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[True] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[Meta, ResultStaging]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[False] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[ExtendedMeta, Result]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[True] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[ExtendedMeta, ResultStaging]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[False] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[Meta, ExplainedResult]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[True] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[Meta, ExplainedResultStaging]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[False] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[ExtendedMeta, ExplainedResult]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[False] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[True] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[ExtendedMeta, ExplainedResultStaging]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[False] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[Meta, MinimalResult]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[True] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[Meta, MinimalResultStaging]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[False] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[ExtendedMeta, MinimalResult]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[False] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[True] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[ExtendedMeta, MinimalResultStaging]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[False] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[Meta, ExplainedMinimalResult]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[False] = ..., staging: Literal[True] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[Meta, ExplainedMinimalResultStaging]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[False] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[ExtendedMeta, ExplainedMinimalResult]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: Literal[True] = ..., explain: Literal[True] = ...,
        extended_meta: Literal[True] = ..., staging: Literal[True] = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[ExtendedMeta, ExplainedMinimalResultStaging]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: bool = ..., explain: bool = ...,
        extended_meta: bool = ..., staging: bool = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Results[
    Union[Meta, ExtendedMeta],
    Union[
        MinimalResult, ExplainedMinimalResult,
        Result, ExplainedResult,
        MinimalResultStaging, ExplainedMinimalResultStaging,
        ResultStaging, ExplainedResultStaging,
    ]
]: ...
