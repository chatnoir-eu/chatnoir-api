from random import uniform
from time import sleep
from typing import Optional, TypeVar, Type
from urllib.parse import urljoin

from pydantic import BaseModel
from requests import Response as HttpResponse, post

from chatnoir_api.constants import BASE_URL
from chatnoir_api.logger import logger
from chatnoir_api.defaults import (
    DEFAULT_RETRIES,
    DEFAULT_BACKOFF_SECONDS,
    DEFAULT_TIMEOUT,
)

_JsonResponse = TypeVar("_JsonResponse", bound=BaseModel)


def request_page(
    request: BaseModel,
    response_type: Type[_JsonResponse],
    endpoint: str,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
    url_for_request: Optional[str] = None,
    non_default_headers: Optional[dict] = None,
) -> _JsonResponse:

    headers = {
        "Accept": "application/json",
        "Content-Type": "text/plain",
    }
    request_json = request.model_dump_json()

    headers = headers if non_default_headers is None else non_default_headers
    url = urljoin(BASE_URL, f"api/v1/{endpoint}")
    if url_for_request is not None:
        url = url_for_request

    raw_response: HttpResponse = post(
        url,
        headers=headers,
        data=request_json.encode("utf-8"),
        timeout=timeout,
    )
    if raw_response.status_code // 100 == 5:
        if retries == 0:
            raise RuntimeError(
                "ChatNoir API internal server error. "
                "Please get in contact with the admins."
            )
        else:
            logger.warning(
                f"ChatNoir API internal server error. "
                f"Retrying in {round(backoff_seconds)} seconds."
            )
            sleep(backoff_seconds)
            return request_page(
                request=request,
                response_type=response_type,
                endpoint=endpoint,
                timeout=timeout,
                retries=retries - 1,
                backoff_seconds=round(backoff_seconds) * 2
                + uniform(-0.5, 0.5),  # nosec: B311
                url_for_request=url_for_request,
                non_default_headers=non_default_headers,
            )
    if raw_response.status_code == 401:
        raise RuntimeError("ChatNoir API key invalid or missing.")
    elif raw_response.status_code == 403:
        raise RuntimeError(
            "ChatNoir API blocked this IP address. "
            "Please get in contact with the admins."
        )
    elif raw_response.status_code == 429:
        if retries == 0:
            raise RuntimeError("ChatNoir API quota exceeded. Please throttle requests.")
        else:
            logger.warning(
                f"ChatNoir API quota exceeded. "
                f"Retrying in {round(backoff_seconds)} seconds."
            )
        sleep(backoff_seconds)
        return request_page(
            request=request,
            response_type=response_type,
            endpoint=endpoint,
            timeout=timeout,
            retries=retries - 1,
            backoff_seconds=round(backoff_seconds) * 2
            + uniform(-0.5, 0.5),  # nosec: B311
            url_for_request=url_for_request,
            non_default_headers=non_default_headers,
        )
    elif not raw_response.ok:
        raise RuntimeError(
            f"ChatNoir API request failed "
            f"with code {raw_response.status_code}."
            f"Please get in contact with the admins.\n{raw_response.text}"
        )

    response_json = raw_response.text
    response = response_type.model_validate_json(response_json)

    return response
