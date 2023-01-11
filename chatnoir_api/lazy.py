from itertools import chain, repeat
from math import ceil
from typing import (
    Iterator, Generic, TypeVar, Optional, List, Callable, Sequence, Any,
    overload, Union
)

from chatnoir_api.logger import logger
from chatnoir_api.model.result import Results, Meta, MinimalResult, \
    ResultsMixin

_ResultType = TypeVar("_ResultType", bound=MinimalResult, covariant=True)
_MetaType = TypeVar("_MetaType", bound=Meta, covariant=True)


class LazyResultPage(
    ResultsMixin[_MetaType, _ResultType],
    Results[_MetaType, _ResultType],
    Generic[_MetaType, _ResultType],
):
    _start: int
    _size: int
    _load_page: Callable[
        [int, int],
        Results[_MetaType, _ResultType]
    ]
    _maybe_response: Optional[Results[_MetaType, _ResultType]] = None

    def __init__(
            self,
            start: int,
            size: int,
            load_page: Callable[
                [int, int],
                Results[_MetaType, _ResultType]
            ],
    ):
        self._start = start
        self._size = size
        self._load_page = load_page

    @property
    def _response(self) -> Results[_MetaType, _ResultType]:
        if self._maybe_response is None:
            self._maybe_response = self._load_page(self._start, self._size)
            if len(self._maybe_response) > self._size:
                raise RuntimeError(
                    "Current page is larger than the page size."
                )
        return self._maybe_response

    @property
    def meta(self) -> _MetaType:
        return self._response.meta

    @property
    def results(self) -> Sequence[_ResultType]:
        return self._response.results


class LazyResultPageList(
    Sequence[LazyResultPage[_MetaType, _ResultType]],
    Generic[_MetaType, _ResultType]
):
    _page_size: int
    _load_page: Callable[[int, int], Results[_MetaType, _ResultType]]

    _pages: List[Optional[LazyResultPage[_MetaType, _ResultType]]]

    def __init__(
            self,
            page_size: int,
            total_results: int,
            load_page: Callable[
                [int, int],
                Results[_MetaType, _ResultType]
            ],
    ):
        self._page_size = page_size
        self._load_page = load_page

        self._pages = list(repeat(
            None,
            ceil(total_results / page_size)
        ))

    @overload
    def __getitem__(self, i: int) -> LazyResultPage[_MetaType, _ResultType]:
        pass

    @overload
    def __getitem__(
            self,
            s: slice
    ) -> Sequence[LazyResultPage[_MetaType, _ResultType]]:
        pass

    def __getitem__(
            self, i: Union[int, slice]
    ) -> Union[
        LazyResultPage[_MetaType, _ResultType],
        Sequence[LazyResultPage[_MetaType, _ResultType]]
    ]:
        if isinstance(i, int):
            if self._pages[i] is None:
                start = i * self._page_size
                self._pages[i] = LazyResultPage(
                    start,
                    self._page_size,
                    self._load_page
                )
            return self._pages[i]
        elif isinstance(i, slice):
            start = i.start
            if start is None:
                start = 0
            if start < 0:
                start = len(self) + start

            stop = i.stop
            if stop is None:
                stop = len(self)
            if stop < 0:
                stop = len(self) + stop

            step = i.step
            if step is None:
                step = 1

            indices = range(start, stop, step)
            return [self[i] for i in indices]
        else:
            raise TypeError("Invalid index type.")

    def __len__(self) -> int:
        return len(self._pages)


class LazyResultSequence(
    Results[_MetaType, _ResultType],
    Generic[_MetaType, _ResultType],
):
    _page_size: int
    _pages: Sequence[LazyResultPage[_MetaType, _ResultType]]

    def __init__(
            self,
            page_size: int,
            load_page: Callable[
                [int, int],
                Results[_MetaType, _ResultType]
            ],
    ):
        self._page_size = page_size
        # Load first page to get total results count.
        first_page = LazyResultPage(
            start=0,
            size=page_size,
            load_page=load_page,
        )
        total_results = first_page.meta.total_results
        # Initialize remaining pages.
        self._pages = LazyResultPageList(
            self._page_size,
            total_results,
            load_page
        )

    @property
    def meta(self) -> _MetaType:
        return self._pages[0].meta

    @property
    def results(self) -> Sequence[_ResultType]:
        return self

    @overload
    def __getitem__(self, i: int) -> _ResultType:
        pass

    @overload
    def __getitem__(self, s: slice) -> Sequence[_ResultType]:
        pass

    def __getitem__(
            self,
            i: Union[int, slice],
    ) -> Union[_ResultType, Sequence[_ResultType]]:
        if isinstance(i, int):
            page_index = i // self._page_size
            page_offset = page_index * self._page_size
            corrected_index = i - page_offset
            page: LazyResultPage[_MetaType, _ResultType] = \
                self._pages[page_index]
            return page[corrected_index]
        elif isinstance(i, slice):
            start = i.start
            if start is None:
                start = 0
            if start < 0:
                start = len(self) + start
                logger.warning(
                    "Iterating search results from the back is unsafe. "
                    "The total result count is an estimate "
                    "and the actual result list might not be that long."
                )

            stop = i.stop
            if stop is None:
                stop = len(self)
            if stop < 0:
                stop = len(self) + stop
                logger.warning(
                    "Iterating search results from the back is unsafe. "
                    "The total result count is an estimate "
                    "and the actual result list might not be that long."
                )

            step = i.step
            if step is None:
                step = 1

            indices = range(start, stop, step)
            return [self[i] for i in indices]
        else:
            raise TypeError("Invalid index type.")

    def index(self, value: Any, start: int = ..., stop: int = ...) -> int:
        for page_index, page in enumerate(self._pages):
            page_offset = page_index * self._page_size
            corrected_start = start - page_offset
            corrected_stop = stop - page_offset
            try:
                # If found, return immediately.
                return page_offset + page.index(
                    value,
                    corrected_start,
                    corrected_stop,
                )
            except ValueError:
                # Ignore, but raise later of not found.
                pass
        raise ValueError("Not found.")

    def count(self, value: Any) -> int:
        return sum(page.count(value) for page in self._pages)

    def __contains__(self, x: object) -> bool:
        return any(x in page for page in self._pages)

    def __iter__(self) -> Iterator[_ResultType]:
        return chain.from_iterable(self._pages)

    def __reversed__(self) -> Iterator[_ResultType]:
        logger.warning(
            "Iterating search results from the back is unsafe. "
            "The total result count is an estimate "
            "and the actual result list might not be that long."
        )
        return chain.from_iterable(
            reversed(page)
            for page in reversed(self._pages)
        )

    def __len__(self) -> int:
        return self.meta.total_results
