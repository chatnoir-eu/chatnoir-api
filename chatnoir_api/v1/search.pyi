from typing import List, Tuple, Union, Set, overload

from chatnoir_api.model import Index
from chatnoir_api.model.result import Meta, MinimalResult, Result, \
    ExplainedResult, ExplainedMinimalResult, ExtendedMeta, Results
from chatnoir_api.v1.model import (
    MinimalResponse, ExplainedMinimalResponse,
    Response, ExplainedResponse,
    MinimalResponseStaging, ExplainedMinimalResponseStaging,
    ResponseStaging, ExplainedResponseStaging,
    ExtendedMetaMinimalResponseStaging,
    ExplainedExtendedMetaMinimalResponseStaging,
    ExtendedMetaResponseStaging, ExplainedExtendedMetaResponseStaging,
    PhraseRequest, PhraseRequestStaging
)


@overload
def search(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: bool = ...,
        explain: bool = ...,
        extended_meta: bool = ...,
        staging: bool = ...,
        page_size: int = ..., retries: int = ..., backoff_seconds: float = ...,
) -> Results[
    Union[Meta, ExtendedMeta],
    List[Union[MinimalResult, ExplainedMinimalResult, Result, ExplainedResult]]
]: ...


@overload
def search_page(
        api_key: str, query: str, index: Union[Index, Set[Index]] = ...,
        minimal: bool = ...,
        explain: bool = ...,
        extended_meta: bool = ...,
        staging: bool = ...,
        start: int = ..., size: int = ..., retries: int = ...,
        backoff_seconds: float = ...,
) -> Tuple[
    Union[Meta, ExtendedMeta],
    List[Union[MinimalResult, ExplainedMinimalResult, Result, ExplainedResult]]
]: ...
