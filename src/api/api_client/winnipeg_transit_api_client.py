import os
from http import HTTPStatus
from typing import Any, NoReturn
import requests
from dotenv import load_dotenv
from api.api_constants import WINNIPEG_TRANSIT_API_STOP_SCHEDULE_BASE_URL, WINNIPEG_TRANSIT_API_TRIP_SCHEDULE_BASE_URL
from api.exceptions.api_request_error import APIConnectionError, APITimeoutError, APIJsonError, APIRedirectError, \
    BadAPIRequestError, APIKeyError, APIAccessError, APIResourceNotFoundError, TooManyAPIRequestsError, APIHTTPError, \
    APIRequestError


load_dotenv()

API_KEY = os.environ["API_KEY"]

def request_stop_schedule(stop_id: str) -> tuple[dict[str, Any], str]:
    """
    Requests the stop schedule for the stop with the given stop ID from the
    Winnipeg Transit API. Throws an exception if there is an error with the
    request; otherwise returns the response as a dictionary along with the
    URL that was used to obtain it.
    """
    return _request_from_api(
        url=f"{WINNIPEG_TRANSIT_API_STOP_SCHEDULE_BASE_URL}/{stop_id}/schedule.json"
    )

def request_trip_schedule(trip_key: str) -> tuple[dict[str, Any], str]:
    """
    Request the trip schedule for the trip with the given trip key from the
    Winnipeg Transit API. Throws an exception if there is an error with the
    request; otherwise returns the response as a dictionary along with the
    URL that was used to obtain it.
    """
    return _request_from_api(
        url=f"{WINNIPEG_TRANSIT_API_TRIP_SCHEDULE_BASE_URL}/{trip_key}.json"
    )

def _request_from_api(url: str) -> tuple[dict[str, Any], str]:
    try:
        response = requests.get(
            url,
            params={
                "api-key": API_KEY,
            },
            timeout=15
        )

        response.raise_for_status()

        if not isinstance(response.json(), dict):
            raise APIJsonError(url)

        return response.json(), url
    except requests.exceptions.RequestException as e:
        _raise_from_requests_exception(e, url)

def _raise_from_requests_exception(
        e: requests.exceptions.RequestException,
        url: str
) -> NoReturn:
    match e:
        case requests.exceptions.Timeout():
            raise APITimeoutError(url)
        case requests.exceptions.ConnectionError():
            raise APIConnectionError(url)
        case requests.exceptions.JSONDecodeError():
            raise APIJsonError(url)
        case requests.exceptions.TooManyRedirects():
            raise APIRedirectError(url)
        case requests.exceptions.HTTPError():
            match e.response.status_code:
                case HTTPStatus.BAD_REQUEST:
                    raise BadAPIRequestError(url)
                case HTTPStatus.UNAUTHORIZED:
                    raise APIKeyError(url)
                case HTTPStatus.FORBIDDEN:
                    raise APIAccessError(url)
                case HTTPStatus.NOT_FOUND:
                    raise APIResourceNotFoundError(url)
                case HTTPStatus.TOO_MANY_REQUESTS:
                    raise TooManyAPIRequestsError(url)

            raise APIHTTPError(url, e.response.status_code)

    raise APIRequestError(url)
