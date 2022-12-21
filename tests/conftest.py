from os import environ

from pytest import fixture, skip

from chatnoir_api import Index
from chatnoir_api.constants import BASE_URL, BASE_URL_STAGING


@fixture(scope="module")
def api_key(base_url: str) -> str:
    key: str
    if base_url == BASE_URL:
        key = "CHATNOIR_API_KEY"
    elif base_url == BASE_URL_STAGING:
        key = "CHATNOIR_API_KEY_STAGING"
    else:
        skip("Unknown base URL")
        raise
    if key not in environ:
        raise RuntimeError(
            f"Must specify ChatNoir api key "
            f"in the {key} environment variable "
            f"to run this test."
        )
    return environ[key]


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
    params=[
        # BASE_URL,
        BASE_URL_STAGING,
    ]
)
def base_url(request) -> str:
    return request.param


@fixture(
    scope="module",
    params=[
        Index.ClueWeb09,
        Index.ClueWeb12,
        Index.ClueWeb22,
        Index.CommonCrawl1511,
        Index.CommonCrawl1704,
    ]
)
def index(request, base_url: str) -> Index:
    if base_url == BASE_URL and request.param == Index.ClueWeb22:
        skip("ClueWeb22 is not available on the production base URL.")
    if base_url == BASE_URL_STAGING and request.param == Index.CommonCrawl1511:
        skip("Common Crawl 15/11 is not available on the staging base URL.")
    if base_url == BASE_URL_STAGING and request.param == Index.CommonCrawl1704:
        skip("Common Crawl 17/04 is not available on the staging base URL.")
    return request.param
