from typing import List

from pytest import fixture

from chatnoir_api import (
    Index, PhraseSearchResult, ResultsMeta, MinimalPhraseSearchResult, Results
)
from chatnoir_api.v1 import search_phrases_page, search_phrases


@fixture(params=[True, False])
def minimal(request) -> bool:
    return request.param


def test_page(api_key: str, query: str, minimal: bool):
    meta, results = search_phrases_page(
        api_key=api_key,
        query=query,
        minimal=minimal,
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
    if minimal:
        assert isinstance(results[0], MinimalPhraseSearchResult)
    else:
        assert isinstance(results[0], PhraseSearchResult)


def test_page_size(api_key: str, query: str, page_size: int, minimal: bool):
    _, results = search_phrases_page(
        api_key=api_key,
        query=query,
        size=page_size,
        minimal=minimal,
    )
    assert len(results) == page_size


def test_explain(api_key: str, query: str, explain: bool):
    _, results = search_phrases_page(
        api_key=api_key,
        query=query,
        size=1,
        explain=explain,
        minimal=False,
    )
    assert len(results) > 0
    if explain:
        assert results[0].explanation is not None
    else:
        assert results[0].explanation is None


def test_index(api_key: str, query: str, index: Index):
    _, results = search_phrases_page(
        api_key=api_key,
        query=query,
        size=1,
        index=index,
        minimal=False,
    )
    assert len(results) > 0
    assert results[0].index == index


def test_iterable(api_key: str, query: str, minimal: bool):
    results = search_phrases(
        api_key=api_key,
        query=query,
        page_size=1,
        minimal=minimal,
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
    if minimal:
        assert isinstance(first_result, MinimalPhraseSearchResult)
    else:
        assert isinstance(first_result, PhraseSearchResult)

    second_result = next(result_iterator, None)
    assert second_result is not None
    if minimal:
        assert isinstance(second_result, MinimalPhraseSearchResult)
    else:
        assert isinstance(second_result, PhraseSearchResult)
