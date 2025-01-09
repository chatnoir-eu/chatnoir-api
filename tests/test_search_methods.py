from chatnoir_api import (
    Meta,
)
from chatnoir_api.v1 import search


def test_default_retrieval_model(api_key: str) -> None:
    results = search(
        api_key=api_key,
        query="how to find a test dataset",
        index="msmarco-document-v2.1",
        search_method="default",
    )

    meta = results.meta

    assert meta is not None
    assert isinstance(meta, Meta)

    assert meta.total_results is not None
    assert isinstance(meta.total_results, int)
    assert meta.total_results == 5517
    assert meta.search_method == "default"


def test_bm25_retrieval_model(api_key: str) -> None:
    results = search(
        api_key=api_key,
        query="how to find a test dataset",
        index="msmarco-document-v2.1",
        search_method="bm25",
    )

    meta = results.meta

    assert meta is not None
    assert isinstance(meta, Meta)

    assert meta.total_results is not None
    assert isinstance(meta.total_results, int)
    assert meta.total_results == 2800000
    assert meta.search_method == "bm25"
