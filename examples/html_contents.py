from uuid import UUID

from chatnoir_api import html_contents
from chatnoir_api.model import Index

contents = html_contents(
    UUID("e635baa8-7341-596a-b3cf-b33c05954361"),
    Index.CommonCrawl1511,
)
print(contents)

plain_contents = html_contents(
    UUID("e635baa8-7341-596a-b3cf-b33c05954361"),
    Index.CommonCrawl1511,
    plain=True,
)
print(plain_contents)
