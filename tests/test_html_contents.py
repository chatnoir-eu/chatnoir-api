from uuid import UUID

from chatnoir_api import html_contents, Index


def test_html_contents_uuid():
    contents = html_contents(
        UUID("e635baa8-7341-596a-b3cf-b33c05954361"),
        Index.CommonCrawl1511,
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert "<title>hello world</title>" in contents


def test_html_contents_plain_uuid():
    contents = html_contents(
        UUID("e635baa8-7341-596a-b3cf-b33c05954361"),
        Index.CommonCrawl1511,
        plain=True,
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert "<title>hello world</title>" in contents


def test_html_contents_document_id():
    contents = html_contents(
        "clueweb09-en0051-90-00849",
        Index.ClueWeb09,
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert "<title>Test, test, test</title>" in contents


def test_html_contents_plain_document_id():
    contents = html_contents(
        "clueweb09-en0051-90-00849",
        Index.ClueWeb09,
        plain=True
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert "<title>Test, test, test</title>" in contents
