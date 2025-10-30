from typing import Sequence

from pytest import fixture

from chatnoir_api import Index, Meta, Results, MinimalResult, \
    Result, ExplainedMinimalResult
from chatnoir_api.v1 import search_page, search


@fixture(params=[True, False])
def minimal(request) -> bool:
    return request.param


def test_page(api_key: str, query: str) -> None:
    results = search_page(
        api_key=api_key,
        query=query,
    )
    meta = results.meta

    assert meta is not None
    assert isinstance(meta, Meta)

    assert meta.query_time is not None
    assert isinstance(meta.query_time, int)
    assert meta.query_time > 0

    assert meta.total_results is not None
    assert isinstance(meta.total_results, int)
    assert meta.total_results > 0

    assert results is not None
    assert isinstance(results, Sequence)
    assert len(results) > 0
    assert len(results) <= meta.total_results

    assert results[0] is not None
    assert isinstance(results[0], MinimalResult)


def test_page_size(api_key: str, query: str, page_size: int) -> None:
    results = search_page(
        api_key=api_key,
        query=query,
        size=page_size,
    )
    assert len(results) == page_size


def test_page_index(api_key: str, query: str, index: Index) -> None:
    results = search_page(
        api_key=api_key,
        query=query,
        size=1,
        index=index,
    )
    assert results[0].index == index


def test_page_minimal(api_key: str, query: str, minimal: bool) -> None:
    results = search_page(
        api_key=api_key,
        query=query,
        size=1,
        minimal=minimal,
    )
    if minimal:
        assert isinstance(results[0], MinimalResult)
    else:
        assert isinstance(results[0], Result)


def test_page_explain(api_key: str, query: str, explain: bool) -> None:
    results = search_page(
        api_key=api_key,
        query=query,
        size=1,
        explain=explain,
    )
    if explain:
        assert isinstance(results[0], ExplainedMinimalResult)

        assert results[0].explanation is not None
        assert results[0].explanation.value is not None
        assert isinstance(results[0].explanation.value, float)
        assert results[0].explanation.description is not None
        assert isinstance(results[0].explanation.description, str)
    else:
        assert isinstance(results[0], MinimalResult)


def test_page_meta(api_key: str, query: str) -> None:
    results = search_page(
        api_key=api_key,
        query=query,
        size=1,
    )
    meta = results.meta

    assert isinstance(meta, Meta)


def test_iterable(api_key: str, query: str) -> None:
    results = search(
        api_key=api_key,
        query=query,
        page_size=1,
    )
    assert results is not None
    assert isinstance(results, Results)

    assert results.meta is not None
    assert isinstance(results.meta, Meta)

    assert results.meta.query_time is not None
    assert isinstance(results.meta.query_time, int)
    assert results.meta.query_time > 0

    assert results.meta.total_results is not None
    assert isinstance(results.meta.total_results, int)
    assert results.meta.total_results > 0

    result_iterator = iter(results)

    first_result = next(result_iterator, None)
    assert first_result is not None
    assert isinstance(first_result, MinimalResult)

    second_result = next(result_iterator, None)
    assert second_result is not None
    assert isinstance(second_result, MinimalResult)


def test_iterable_index(api_key: str, query: str, index: Index) -> None:
    results = search(
        api_key=api_key,
        query=query,
        page_size=1,
        index=index,
        minimal=False,
    )
    assert results[0].index == index


def test_iterable_minimal(api_key: str, query: str, minimal: bool) -> None:
    results = search(
        api_key=api_key,
        query=query,
        page_size=1,
        minimal=minimal,
    )
    if minimal:
        assert isinstance(results[0], MinimalResult)
    else:
        assert isinstance(results[0], Result)


def test_iterable_explain(api_key: str, query: str, explain: bool) -> None:
    results = search(
        api_key=api_key,
        query=query,
        page_size=1,
        explain=explain,
    )

    if explain:
        assert isinstance(results[0], ExplainedMinimalResult)

        assert results[0].explanation is not None
        assert results[0].explanation.value is not None
        assert isinstance(results[0].explanation.value, float)
        assert results[0].explanation.description is not None
        assert isinstance(results[0].explanation.description, str)
    else:
        assert isinstance(results[0], MinimalResult)


def test_iterable_meta(api_key: str, query: str) -> None:
    results = search(
        api_key=api_key,
        query=query,
        page_size=1,
    )

    assert isinstance(results.meta, Meta)
