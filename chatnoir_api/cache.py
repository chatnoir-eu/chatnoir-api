from typing import Union
from urllib.parse import urljoin
from uuid import UUID, uuid5, NAMESPACE_URL
import json

from requests import get, Response

from chatnoir_api.constants import BASE_URL, BASE_URL_STAGING
from chatnoir_api.model import Index


def cache_contents(
        uuid_or_document_id: Union[UUID, str],
        index: Index,
        plain: bool = False,
        staging: bool = False,
) -> str:
    uuid: UUID
    if isinstance(uuid_or_document_id, str):
        uuid = uuid5(NAMESPACE_URL, f"{index.prefix}:{uuid_or_document_id}")
    else:
        uuid = uuid_or_document_id

    base_url = BASE_URL_STAGING if staging else BASE_URL
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

    if index in (Index.MSMarcoV21, Index.MSMarcoV21Segmented):
        ret = json.loads(response.text)
        if uuid_or_document_id != ret['docid']:
            raise ValueError(f'Document Id is not as expected. Expected "{uuid_or_document_id}" but have "{ret["docid"]}".')
        return ret

    return response.text
