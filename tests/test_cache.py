from uuid import UUID

from chatnoir_api import cache_contents, Index, ShortUUID


def test_html_contents_trec_id():
    contents = cache_contents(
        "clueweb09-en0051-90-00849",
        Index.ClueWeb09,
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert "<title>Test, test, test</title>" in contents


def test_html_contents_plain_trec_id():
    contents = cache_contents(
        "clueweb09-en0051-90-00849",
        Index.ClueWeb09,
        plain=True
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert "<title>Test, test, test</title>" in contents


def test_html_contents_uuid():
    contents = cache_contents(
        UUID("e635baa8-7341-596a-b3cf-b33c05954361"),
        Index.CommonCrawl1511,
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert "<title>hello world</title>" in contents


def test_html_contents_plain_uuid():
    contents = cache_contents(
        UUID("e635baa8-7341-596a-b3cf-b33c05954361"),
        Index.CommonCrawl1511,
        plain=True,
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert "<title>hello world</title>" in contents


def test_html_contents_short_uuid():
    contents = cache_contents(
        ShortUUID("f6J0lMPmVfWs19jJNQkHKA"),
        Index.ClueWeb22,
        base_url="https://chatnoir.web.webis.de/"
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert "<title data-dcnode-id=\"1108\">" \
           "Hello World | Codecademy</title>" in contents


def test_html_contents_plain_short_uuid():
    contents = cache_contents(
        ShortUUID("f6J0lMPmVfWs19jJNQkHKA"),
        Index.ClueWeb22,
        plain=True,
        base_url="https://chatnoir.web.webis.de/"
    )

    assert contents is not None
    assert isinstance(contents, str)
    assert "Hello World" in contents
