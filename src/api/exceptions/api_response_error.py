from typing import Any


class APIResponseError(Exception):
    """
    Exception thrown when a response from Winnipeg Transit's API is invalid.
    """

    def __init__(self, api_resource_url: str):
        self._api_resource_url = api_resource_url

    @property
    def api_resource_url(self) -> str:
        return self._api_resource_url

class APIResponseAttributeError(APIResponseError):
    """
    Exception thrown when an attribute read from Winnipeg Transit's API
    response is unexpectedly missing or invalid.
    """

    def __init__(
        self,
        api_resource_url: str,
        attribute_name: str
    ):
        super().__init__(api_resource_url)

        self._attribute_name = attribute_name

    @property
    def attribute_name(self) -> str:
        return self._attribute_name

class MissingAPIResponseAttributeError(APIResponseAttributeError):
    pass

class InvalidAPIResponseAttributeError(APIResponseAttributeError):
    def __init__(
        self,
        api_resource_url: str,
        attribute_name: str,
        invalid_token: str
    ):
        super().__init__(api_resource_url, attribute_name)

        self._invalid_token = invalid_token

    @property
    def invalid_token(self) -> str:
        return self._invalid_token

class MalformedAPIResponseAttributeError(InvalidAPIResponseAttributeError):
    pass

class IllegalAPIResponseAttributeError(InvalidAPIResponseAttributeError):
    pass

class APIAttributeCombinationError(APIResponseError):
    """
    Exception thrown when an illogical set of attributes is returned from
    Winnipeg Transit's API.
    """

    def __init__(
        self,
        api_resource_url: str,
        invalid_attributes: list[Any]
    ):
        super().__init__(api_resource_url)

        self._invalid_attributes = invalid_attributes

    @property
    def invalid_attributes(self) -> list[Any]:
        return self._invalid_attributes