from typing import Union, Any
from urllib.parse import urljoin
from uuid import UUID, uuid5, NAMESPACE_URL

from requests import get, Response

from chatnoir_api.constants import BASE_URL, BASE_URL_WEBCONTENT
from chatnoir_api.defaults import DEFAULT_TIMEOUT
from chatnoir_api.model import Index, index_id, index_prefix


def cache_contents(
    uuid_or_document_id: Union[UUID, str],
    index: Index,
    plain: bool = False,
    timeout: int = DEFAULT_TIMEOUT,
) -> str:
    uuid: UUID
    if isinstance(uuid_or_document_id, str):
        uuid = uuid5(NAMESPACE_URL, f"{index_prefix(index)}:{uuid_or_document_id}")
    else:
        uuid = uuid_or_document_id

    response: Response = get(
        urljoin(BASE_URL, "cache"),
        params={
            "uuid": str(uuid),
            "index": index_id(index),
            "raw": "true",
            "plain": "true" if plain else "false",
        },
        timeout=timeout,
    )
    response.raise_for_status()
    return response.text


def term_vectors(
    trec_id: str,
    index: Index,
    timeout: int = DEFAULT_TIMEOUT,
) -> Any:
    response: Response = get(
        urljoin(BASE_URL_WEBCONTENT, "_termvectors"),
        params={
            "trec-id": trec_id,
            "index": index_id(index),
        },
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()
