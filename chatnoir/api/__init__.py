from uuid import UUID

from requests import get, Response

from chatnoir.api.constants import BASE_URL
from chatnoir.model import Index


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
