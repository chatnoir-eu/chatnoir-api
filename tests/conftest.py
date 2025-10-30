from os import environ

from pytest import fixture

from chatnoir_api import Index


@fixture(scope="module")
def api_key() -> str:
    key = "CHATNOIR_API_KEY"
    if key not in environ:
        raise RuntimeError(
            f"Must specify ChatNoir API key "
            f"in the {key} environment variable "
            f"to run this test."
        )
    return environ[key]


@fixture(scope="module")
def api_key_chat() -> str:
    key = "CHATNOIR_API_KEY_CHAT"
    if key not in environ:
        raise RuntimeError(
            f"Must specify ChatNoir Chat API key "
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
        "clueweb09",
        "clueweb12",
        "clueweb22/b",
        "msmarco-document",
        "msmarco-passage",
        "msmarco-document-v2",
        "msmarco-passage-v2",
        "msmarco-document-v2.1",
        "msmarco-passage-v2.1",
        "trec-tot/2024",
        "longeval-sci/2024-11",
        "wows-owi/2025",
    ],
)
def index(request) -> Index:
    return request.param
