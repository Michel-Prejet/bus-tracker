class APIResponseAttributeError(Exception):
    """
    Exception thrown when an attribute read from Winnipeg Transit's API
    response is unexpectedly missing or invalid.
    """
    def __init__(
        self,
        api_resource_name: str,
        attribute_name: str
    ):
        self._api_resource_name = api_resource_name
        self._attribute_name = attribute_name

    @property
    def api_resource_name(self) -> str:
        return self._api_resource_name

    @property
    def attribute_name(self) -> str:
        return self._attribute_name

class MissingAPIResponseAttributeError(APIResponseAttributeError):
    pass

class MalformedAPIResponseAttributeError(APIResponseAttributeError):
    def __init__(
        self,
        api_resource_name: str,
        attribute_name: str,
        invalid_token: str
    ):
        super().__init__(api_resource_name, attribute_name)

        self._invalid_token = invalid_token

    @property
    def invalid_token(self) -> str:
        return self._invalid_token