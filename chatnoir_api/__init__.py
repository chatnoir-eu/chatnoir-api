__version__ = "0.1.6"

from logging import getLogger
from uuid import UUID

from requests import get, Response

from chatnoir_api.constants import BASE_URL
from chatnoir_api.model import Index

logger = getLogger("chatnoir-api")


def html_contents(
        uuid: UUID,
        index: Index,
        plain: bool = False,
) -> str:
    response: Response = get(
        f"{BASE_URL}/cache",
        params={
            "uuid": str(uuid),
            "index": index.value,
            "raw": True,
            "plain": plain,
        }
    )
    return response.text
