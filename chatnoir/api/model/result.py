from abc import ABC
from typing import Sized, TypeVar, Generic, Optional, Dict, Iterable
from uuid import UUID

from chatnoir.api import html_contents
from chatnoir.api.model import Index
from chatnoir.api.model.highlight import HighlightedText


class Result(ABC):
    score: float = NotImplemented
    uuid: UUID = NotImplemented
    target_uri: str = NotImplemented
    snippet: HighlightedText = NotImplemented


# noinspection DuplicatedCode
class SearchResult(Result):
    index: Index = NotImplemented
    trec_id: Optional[str] = NotImplemented
    target_hostname: str = NotImplemented
    page_rank: Optional[float] = NotImplemented
    spam_rank: Optional[float] = NotImplemented
    title: HighlightedText = NotImplemented
    explanation: Optional[Dict] = NotImplemented

    def html_contents(self, plain: bool = False) -> str:
        return html_contents(self.uuid, self.index, plain)


class MinimalPhraseSearchResult(Result, ABC):
    pass


# noinspection DuplicatedCode
class PhraseSearchResult(MinimalPhraseSearchResult):
    index: Index = NotImplemented
    trec_id: Optional[str] = NotImplemented
    target_hostname: str = NotImplemented
    page_rank: Optional[float] = NotImplemented
    spam_rank: Optional[float] = NotImplemented
    title: HighlightedText = NotImplemented
    explanation: Optional[Dict] = NotImplemented

    def html_contents(self, plain: bool = False) -> str:
        return html_contents(self.uuid, self.index, plain)


class ResultsMeta(ABC):
    query_time: int = NotImplemented
    total_results: int = NotImplemented


ResultType = TypeVar("ResultType", bound=Result)


class Results(
    Sized,
    Iterable[ResultType],
    Generic[ResultType],
    ResultsMeta,
    ABC
):
    def __len__(self) -> int:
        # pylint: disable=E0303
        total_results = self.total_results
        if total_results is None:
            raise RuntimeError("No total results count was given.")
        elif not isinstance(total_results, int):
            raise RuntimeError("Invalid total results count was given.")
        elif total_results < 0:
            raise RuntimeError(
                "Negative total results count is not supported."
            )
        else:
            # noqa: E0303
            return total_results


class SearchResults(Results[SearchResult], ABC):
    pass


class MinimalPhraseSearchResults(Results[MinimalPhraseSearchResult], ABC):
    pass


class PhraseSearchResults(Results[PhraseSearchResult], ABC):
    pass
