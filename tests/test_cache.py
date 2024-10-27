from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from pytest import fixture, skip

from chatnoir_api import cache_contents, ShortUUID, Index


@dataclass(frozen=True)
class _TestCase:
    index: Index
    uuid: UUID
    trec_id: Optional[str]
    contains_raw: str
    contains_plain: str


@fixture(
    scope="module",
    params=[
        _TestCase(
            "clueweb09",
            ShortUUID("6svePe3PXteDeGPk1XqTLA"),
            "clueweb09-enwp03-01-23789",
            """Test and Test-and-set""",
            "Test and Test-and-set",
        ),
        _TestCase(
            "clueweb12",
            ShortUUID("f0dhEFj9VpixBIspw6xtVQ"),
            "clueweb12-0200wb-93-16911",
            """<title>Test, test, test</title>""",
            "Test, test, test",
        ),
        _TestCase(
            "clueweb22/b",
            ShortUUID("UvPR6h5AWnCcnGoQSTQZTw"),
            "clueweb22-en0044-06-02359",
            """<title data-dcnode-id="184">Hello World!</title>""",
            "Hello World!",
        ),
        _TestCase(
            "msmarco-document-v2.1",
            ShortUUID("RPcdaMiaUFqd4x4qZgkAjQ"),
            "msmarco_v2.1_doc_18_2701526052",
            """"title": "Test - Wikipedia",""",
            "Test - Wikipedia",
        ),
        _TestCase(
            "msmarco-passage-v2.1",
            ShortUUID("JLNEtARbVQqPi1fxu4AbwQ"),
            "msmarco_v2.1_doc_18_2701526052#0_3051069337",
            """"title": "Test - Wikipedia",""",
            "Test - Wikipedia",
        ),
        _TestCase(
            "trec-tot/2024",
            ShortUUID("sH2tKdt-WBKNwfAVfaWW8A"),
            "23949652",
            """"title": "Zack Test",""",
            "Zack Test",
        ),
        # TODO: Add test for `vaswani`.
    ],
)
def test_case(request) -> _TestCase:
    return request.param


def test_cache_contents_trec_id(test_case: _TestCase) -> None:
    if test_case.trec_id is None:
        skip("Test case does not have WARC ID.")

    contents = cache_contents(
        uuid_or_document_id=test_case.trec_id,
        index=test_case.index,
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert test_case.contains_raw in contents


def test_cache_contents_plain_trec_id(test_case: _TestCase) -> None:
    if test_case.trec_id is None:
        skip("Test case does not have WARC ID.")

    contents = cache_contents(
        uuid_or_document_id=test_case.trec_id,
        index=test_case.index,
        plain=True,
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert test_case.contains_plain in contents


def test_cache_contents_uuid(test_case: _TestCase) -> None:
    contents = cache_contents(
        uuid_or_document_id=test_case.uuid,
        index=test_case.index,
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert test_case.contains_raw in contents


def test_cache_contents_plain_uuid(test_case: _TestCase) -> None:
    contents = cache_contents(
        uuid_or_document_id=test_case.uuid,
        index=test_case.index,
        plain=True,
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert test_case.contains_plain in contents
