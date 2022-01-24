from typing import List

from chatnoir_api import Index, SearchResult, ResultsMeta, Results
from chatnoir_api.v1 import search_page, search


def test_page(api_key: str, query: str):
    meta, results = search_page(
        api_key=api_key,
        query=query,
    )
    assert meta is not None
    assert isinstance(meta, ResultsMeta)

    assert meta.query_time is not None
    assert isinstance(meta.query_time, int)
    assert meta.query_time > 0

    assert meta.total_results is not None
    assert isinstance(meta.total_results, int)
    assert meta.total_results > 0

    assert results is not None
    assert isinstance(results, List)
    assert len(results) > 0
    assert len(results) <= meta.total_results

    assert results[0] is not None
    assert isinstance(results[0], SearchResult)


def test_page_size(api_key: str, query: str, page_size: int):
    _, results = search_page(
        api_key=api_key,
        query=query,
        size=page_size,
    )
    assert len(results) == page_size


def test_explain(api_key: str, query: str, explain: bool):
    _, results = search_page(
        api_key=api_key,
        query=query,
        size=1,
        explain=explain,
    )
    assert len(results) > 0
    if explain:
        assert results[0].explanation is not None
    else:
        assert results[0].explanation is None


def test_index(api_key: str, query: str, index: Index):
    _, results = search_page(
        api_key=api_key,
        query=query,
        size=1,
        index=index,
    )
    assert len(results) > 0
    assert results[0].index == index


def test_iterable(api_key: str, query: str):
    results = search(
        api_key=api_key,
        query=query,
        page_size=1,
    )
    assert results is not None
    assert isinstance(results, Results)

    assert results.query_time is not None
    assert isinstance(results.query_time, int)
    assert results.query_time > 0

    assert results.total_results is not None
    assert isinstance(results.total_results, int)
    assert results.total_results > 0

    result_iterator = iter(results)

    first_result = next(result_iterator, None)
    assert first_result is not None
    assert isinstance(first_result, SearchResult)

    second_result = next(result_iterator, None)
    assert second_result is not None
    assert isinstance(second_result, SearchResult)
