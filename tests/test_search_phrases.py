from typing import Sequence

from pytest import fixture

from chatnoir_api import (
    Index, Results, Meta, MinimalResult, Result, ExtendedMeta,
    ExplainedMinimalResult
)
from chatnoir_api.v1 import search_phrases_page, search_phrases


@fixture(params=[True, False])
def minimal(request) -> bool:
    return request.param


def test_page(api_key: str, query: str, staging: bool):
    results = search_phrases_page(
        api_key=api_key,
        query=query,
        staging=staging,
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


def test_page_size(api_key: str, query: str, page_size: int, staging: bool):
    results = search_phrases_page(
        api_key=api_key,
        query=query,
        size=page_size,
        staging=staging,
    )
    assert len(results) == page_size


def test_page_index(api_key: str, query: str, index: Index, staging: bool):
    results = search_phrases_page(
        api_key=api_key,
        query=query,
        size=1,
        index=index,
        minimal=False,
        staging=staging,
    )
    assert results[0].index == index


def test_page_minimal(api_key: str, query: str, minimal: bool, staging: bool):
    results = search_phrases_page(
        api_key=api_key,
        query=query,
        size=1,
        minimal=minimal,
        staging=staging,
    )
    if minimal:
        assert isinstance(results[0], MinimalResult)
    else:
        assert isinstance(results[0], Result)


def test_page_explain(api_key: str, query: str, explain: bool, staging: bool):
    results = search_phrases_page(
        api_key=api_key,
        query=query,
        size=1,
        explain=explain,
        staging=staging,
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


def test_page_meta(api_key: str, query: str, extended_meta: bool,
                   staging: bool):
    results = search_phrases_page(
        api_key=api_key,
        query=query,
        size=1,
        extended_meta=extended_meta,
        staging=staging,
    )
    meta = results.meta

    if extended_meta:
        assert isinstance(meta, ExtendedMeta)
    else:
        assert isinstance(meta, Meta)


def test_iterable(api_key: str, query: str, staging: bool):
    results = search_phrases(
        api_key=api_key,
        query=query,
        page_size=1,
        staging=staging,
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


def test_iterable_index(api_key: str, query: str, index: Index, staging: bool):
    results = search_phrases(
        api_key=api_key,
        query=query,
        page_size=1,
        index=index,
        minimal=False,
        staging=staging,
    )
    assert results[0].index == index


def test_iterable_minimal(api_key: str, query: str, minimal: bool,
                          staging: bool):
    results = search_phrases(
        api_key=api_key,
        query=query,
        page_size=1,
        minimal=minimal,
        staging=staging,
    )
    if minimal:
        assert isinstance(results[0], MinimalResult)
    else:
        assert isinstance(results[0], Result)


def test_iterable_explain(api_key: str, query: str, explain: bool,
                          staging: bool):
    results = search_phrases(
        api_key=api_key,
        query=query,
        page_size=1,
        explain=explain,
        staging=staging,
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


def test_iterable_meta(api_key: str, query: str, extended_meta: bool,
                       staging: bool):
    results = search_phrases(
        api_key=api_key,
        query=query,
        page_size=1,
        extended_meta=extended_meta,
        staging=staging,
    )

    if extended_meta:
        assert isinstance(results.meta, ExtendedMeta)
    else:
        assert isinstance(results.meta, Meta)
