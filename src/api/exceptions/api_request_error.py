from http import HTTPStatus


class APIRequestError(Exception):
    """
    Exception thrown when an error occurred while receiving a request from the
    Winnipeg Transit API.
    """
    def __init__(self, api_resource_url: str):
        self._api_resource_url = api_resource_url

    @property
    def api_resource_url(self) -> str:
        return self._api_resource_url

class APIConnectionError(APIRequestError):
    pass

class APITimeoutError(APIRequestError):
    pass

class APIJsonError(APIRequestError):
    pass

class APIRedirectError(APIRequestError):
    pass

class APIHTTPError(APIRequestError):
    def __init__(self, api_resource_url, http_status: int):
        super().__init__(api_resource_url)

        self._http_status = http_status

    @property
    def http_status(self) -> int:
        return self._http_status

class BadAPIRequestError(APIHTTPError):
    def __init__(self, api_resource_url: str):
        super().__init__(api_resource_url, HTTPStatus.BAD_REQUEST)

class APIKeyError(APIHTTPError):
    def __init__(self, api_resource_url: str):
        super().__init__(api_resource_url, HTTPStatus.UNAUTHORIZED)

class APIAccessError(APIHTTPError):
    def __init__(self, api_resource_url: str):
        super().__init__(api_resource_url, HTTPStatus.FORBIDDEN)

class APIResourceNotFoundError(APIHTTPError):
    def __init__(self, api_resource_url: str):
        super().__init__(api_resource_url, HTTPStatus.NOT_FOUND)

class TooManyAPIRequestsError(APIHTTPError):
    def __init__(self, api_resource_url: str):
        super().__init__(api_resource_url, HTTPStatus.TOO_MANY_REQUESTS)