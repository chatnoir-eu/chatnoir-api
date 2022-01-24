from random import uniform
from time import sleep
from typing import TypeVar, Type

from dataclasses_json import DataClassJsonMixin
from requests import Response as HttpResponse, post

from chatnoir_api.constants import API_V1_URL
from chatnoir_api.logging import logger
from chatnoir_api.v1.defaults import DEFAULT_RETRIES, DEFAULT_BACKOFF_SECONDS

from chatnoir_api.v1.model import Request, Response

_JsonRequest = TypeVar("_JsonRequest", Request, DataClassJsonMixin)
_JsonResponse = TypeVar("_JsonResponse", Response, DataClassJsonMixin)


def request_page(
        request: _JsonRequest,
        response_type: Type[_JsonResponse],
        endpoint: str,
        retries: int = DEFAULT_RETRIES,
        backoff_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> _JsonResponse:
    request_json = request.to_json()

    headers = {
        "Accept": "application/json",
        "Content-Type": "text/plain",
    }
    raw_response: HttpResponse = post(
        f"{API_V1_URL}/{endpoint}",
        headers=headers,
        data=request_json.encode("utf-8")
    )
    if raw_response.status_code // 100 == 5:
        if retries == 0:
            raise RuntimeError(
                "ChatNoir API internal server error. "
                "Please get in contact with the admins "
                "at https://chatnoir.eu/doc/"
            )
        else:
            logger.warning(
                f"ChatNoir API internal server error. "
                f"Retrying in {round(backoff_seconds)} seconds."
            )
            sleep(backoff_seconds)
            return request_page(
                request,
                response_type,
                endpoint,
                retries - 1,
                round(backoff_seconds) * 2 + uniform(-0.5, 0.5)
            )
    if raw_response.status_code == 401:
        raise RuntimeError(
            "ChatNoir API key invalid or missing. "
            "Please refer to the documentation at https://chatnoir.eu/doc/api/"
        )
    elif raw_response.status_code == 403:
        raise RuntimeError(
            "ChatNoir API blocked this IP address. "
            "Please get in contact with the admins at https://chatnoir.eu/doc/"
        )
    elif raw_response.status_code == 429:
        if retries == 0:
            raise RuntimeError(
                "ChatNoir API quota exceeded. Please throttle requests and "
                "refer to the documentation at https://chatnoir.eu/doc/api/"
            )
        else:
            logger.warning(
                f"ChatNoir API quota exceeded. "
                f"Retrying in {round(backoff_seconds)} seconds."
            )
        sleep(backoff_seconds)
        return request_page(
            request,
            response_type,
            endpoint,
            retries - 1,
            round(backoff_seconds) * 2 + uniform(-0.5, 0.5)
        )
    elif not raw_response.ok:
        raise RuntimeError(
            f"ChatNoir API request failed "
            f"with code {raw_response.status_code}."
            f"Please refer to the documentation at https://chatnoir.eu/doc/ "
            f"or get in contact with the admins."
        )

    response_json = raw_response.text
    response = response_type.from_json(response_json)

    return response
