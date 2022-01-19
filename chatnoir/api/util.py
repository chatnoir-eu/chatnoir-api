from abc import ABC, abstractmethod
from typing import Iterator, Generic, TypeVar, Optional, Tuple, List

from chatnoir import logger
from chatnoir.model.result import Results, ResultsMeta, Result, SearchResult

LazyResultType = TypeVar("LazyResultType", bound=Result)


class LazyResults(
    Iterator[LazyResultType],
    Results[LazyResultType],
    Generic[LazyResultType],
    ABC,
):
    _size: int

    def __init__(self, size: int):
        self._size = size

    _next_response_start: int = 0
    _next_index: int = 0
    _last_response: Optional[Tuple[ResultsMeta, List[LazyResultType]]] = None

    @property
    def _last_meta(self) -> Optional[ResultsMeta]:
        if self._last_response is None:
            return None
        meta, _ = self._last_response
        return meta

    @property
    def _last_results(self) -> Optional[List[LazyResultType]]:
        if self._last_response is None:
            return None
        _, results = self._last_response
        return results

    @property
    def _should_load_next_page(self) -> bool:
        return self._next_index == self._next_response_start

    @property
    def _has_next_page(self) -> bool:
        return (
                self._last_results is None or
                len(self._last_results) == self._size
        )

    @abstractmethod
    def page(
            self,
            start: int,
            size: int
    ) -> Tuple[ResultsMeta, List[LazyResultType]]:
        pass

    def _load_next_page(self):
        if not self._has_next_page:
            return RuntimeError(
                "Should only load next result page if there is a next page."
            )

        next_response: Tuple[ResultsMeta, List[LazyResultType]] = self.page(
            start=self._next_response_start,
            size=self._size,
        )
        next_meta: ResultsMeta
        next_results: List[SearchResult]
        next_meta, next_results = next_response

        if (
                self._last_meta is not None and
                self._last_meta.total_results != next_meta.total_results
        ):
            raise RuntimeError(
                f"Total result count of current page "
                f"does not match total result count from previous page: "
                f"{next_meta.total_results} ≠ {self._last_meta.total_results}"
            )
        if len(next_results) > self._size:
            raise RuntimeError("Current page is larger than the page size.")

        self._last_response = next_response
        self._next_response_start += self._size

    def __next__(self) -> LazyResultType:
        if self._should_load_next_page:
            if not self._has_next_page:
                raise StopIteration()
            self._load_next_page()
        last_result_index = (
                self._next_index - self._next_response_start + self._size
        )
        if last_result_index >= len(self._last_results):
            raise StopIteration()

        result = self._last_results[last_result_index]

        self._next_index += 1
        return result

    @property
    def query_time(self) -> int:
        logger.warning(
            "Note that query_time returns the current page's query time. "
            "It is not recommended to use it "
            "unless you monitor query times constantly."
        )
        if self._should_load_next_page:
            self._load_next_page()
        return self._last_meta.query_time

    @property
    def total_results(self) -> int:
        if self._should_load_next_page:
            self._load_next_page()
        return self._last_meta.total_results
