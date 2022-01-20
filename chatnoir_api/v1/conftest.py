from os import environ
from typing import List, Iterator

from pytest import fixture

from chatnoir_api import Index
from chatnoir_api.model.result import SearchResult, ResultsMeta, SearchResults
from chatnoir_api.v1 import search_page, search


@fixture(scope="module")
def api_key() -> str:
    if "CHATNOIR_API_KEY" not in environ:
        raise RuntimeError(
            "Must specify ChatNoir api key "
            "in the CHATNOIR_API_KEY environment variable "
            "to run this test."
        )
    return environ["CHATNOIR_API_KEY"]


@fixture(scope="module", params=["python library", "search engine"])
def query(request) -> str:
    return request.param


@fixture(scope="module", params=[1, 5])
def page_size(request) -> int:
    return request.param


@fixture(scope="module", params=[True, False])
def explain(request) -> bool:
    return request.param


@fixture(
    scope="module",
    params=[Index.ClueWeb09, Index.ClueWeb12, Index.CommonCrawl1511]
)
def index(request) -> Index:
    return request.param
