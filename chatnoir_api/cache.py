from typing import Union
from urllib.parse import urljoin
from uuid import UUID, uuid5, NAMESPACE_URL

from requests import get, Response

from chatnoir_api.constants import BASE_URL
from chatnoir_api.model import Index


def cache_contents(
        uuid_or_document_id: Union[UUID, str],
        index: Index,
        plain: bool = False,
        base_url: str = BASE_URL,
) -> str:
    uuid: UUID
    if isinstance(uuid_or_document_id, str):
        uuid = uuid5(NAMESPACE_URL, f"{index.prefix}:{uuid_or_document_id}")
    else:
        uuid = uuid_or_document_id

    response: Response = get(
        urljoin(base_url, "cache"),
        params={
            "uuid": str(uuid),
            "index": index.value,
            "raw": True,
            "plain": plain,
        }
    )
    response.raise_for_status()
    return response.text
