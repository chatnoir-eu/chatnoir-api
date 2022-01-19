from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import List, Any
from typing import Optional, Set

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class _Request:
    api_key: str
    query: str
    index: Set[str]
    page_from: Optional[int]
    page_size: Optional[int]
    explain: bool


@dataclass_json
@dataclass
class _SearchRequest(_Request):
    pass


@dataclass_json
@dataclass
class _PhraseSearchRequestBase(_Request, ABC):
    slop: Optional[int]

    @property
    @abstractmethod
    def minimal(self) -> bool:
        pass


@dataclass_json
@dataclass
class _MinimalPhraseSearchRequest(_PhraseSearchRequestBase):
    minimal: True


@dataclass_json
@dataclass
class _PhraseSearchRequest(_PhraseSearchRequestBase):
    minimal: False


@dataclass_json
@dataclass
class _ResponseMeta:
    query_time: int
    total_results: int
    indices: Set[str]


@dataclass_json
@dataclass
class _SearchResponseMeta(_ResponseMeta):
    pass


@dataclass_json
@dataclass
class _PhraseSearchResponseMeta(_ResponseMeta):
    pass


@dataclass_json
@dataclass
class _MinimalPhraseSearchResponseMeta(_ResponseMeta):
    pass


@dataclass_json
@dataclass
class _ResponseResult:
    score: float
    uuid: str
    target_uri: str
    snippet: str


@dataclass_json
@dataclass
class _SearchResponseResult(_ResponseResult):
    index: str
    trec_id: Optional[str]
    target_hostname: str
    page_rank: Optional[float]
    spam_rank: Optional[float]
    title: str
    explanation: Any


@dataclass_json
@dataclass
class _MinimalPhraseSearchResponseResult(_ResponseResult):
    pass


@dataclass_json
@dataclass
class _PhraseSearchResponseResult(_MinimalPhraseSearchResponseResult):
    index: str
    trec_id: Optional[str]
    target_hostname: str
    page_rank: Optional[float]
    spam_rank: Optional[float]
    title: str
    explanation: Any


@dataclass_json
@dataclass
class _Response:
    meta: _ResponseMeta
    results: List[_ResponseResult]


@dataclass_json
@dataclass
class _SearchResponse(_Response):
    results: List[_SearchResponseResult]


@dataclass_json
@dataclass
class _MinimalPhraseSearchResponse(_Response):
    results: List[_MinimalPhraseSearchResponseResult]


@dataclass_json
@dataclass
class _PhraseSearchSearchResponse(_Response):
    results: List[_PhraseSearchResponseResult]
