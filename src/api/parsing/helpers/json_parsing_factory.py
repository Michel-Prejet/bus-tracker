from __future__ import annotations
from types import UnionType
from typing import Any, Callable, get_args
from api.exceptions.api_response_attribute_error import MissingAPIResponseAttributeError, \
    MalformedAPIResponseAttributeError
from global_packages.exceptions.value_parsing_error import ValueParsingError


class JsonParsingFactory:
    """
    Retrieves, parses, and performs type validation on fields of a given root
    dictionary. Supports chained calls to navigate through many levels of the
    dictionary at once, including through lists. Applies a given parser and
    validates the type of attributes before they are retrieved.
    """

    def __init__(self, api_resource_url: str, root: dict[str, Any]):
        self._api_resource_url = api_resource_url
        self._root = root

    def next(
            self,
            key: str,
            optional: bool = False
    ) -> JsonParsingFactory | None:
        """
        Returns a JsonParsingFactory with the value specified by the given key
        as its root. This value must be a dictionary, otherwise an exception
        is thrown. If it is None, an exception is thrown only if it is not
        optional, otherwise None is returned.
        """
        next_level = self._root.get(key)

        malformed_exception = MalformedAPIResponseAttributeError(
            api_resource_url=self._api_resource_url,
            attribute_name=key,
            invalid_token=next_level
        )

        if next_level is None:
            if optional:
                return None

            raise MissingAPIResponseAttributeError(
                api_resource_url=self._api_resource_url,
                attribute_name=key
            )

        if type(next_level) is not dict:
            raise malformed_exception

        return JsonParsingFactory(
            api_resource_url=self._api_resource_url,
            root=next_level
        )

    def next_as_list(
        self,
        key: str,
        optional: bool = False
    ) -> list[JsonParsingFactory] | None:
        """
        Returns a list of JsonParsingFactories with the list of values
        specified by the given key as their roots. The value returned by the
        key must be a list, and its elements must be dictionaries, otherwise
        an exception is thrown. If the list is None, an exception is thrown only
        if it is not optional, otherwise None is returned.
        """
        next_level = self._root.get(key)

        malformed_exception = MalformedAPIResponseAttributeError(
            api_resource_url=self._api_resource_url,
            attribute_name=key,
            invalid_token=next_level
        )

        if next_level is None:
            if optional:
                return None

            raise MissingAPIResponseAttributeError(
                api_resource_url=self._api_resource_url,
                attribute_name=key
            )

        if type(next_level) is not list:
            raise malformed_exception

        for element in next_level:
            if type(element) is not dict:
                raise malformed_exception

        return [
            JsonParsingFactory(
                self._api_resource_url,
                element
            )
            for element in next_level
        ]

    def get(
        self,
        key: str,
        expected_type: type | UnionType,
        parser: Callable[[Any], Any] | None = None,
        optional: bool = False
    ) -> Any:
        """
        Returns the value in this dictionary accessed by the given key,
        with the given parser applied. If the value is not of the expected type,
        or the parser throws a ValueParsingException, an exception is thrown. If
        the value is None, an exception is thrown only if it is not optional,
        otherwise None is returned.
        """
        raw_attribute = self._root.get(key)

        malformed_exception = MalformedAPIResponseAttributeError(
            api_resource_url=self._api_resource_url,
            attribute_name=key,
            invalid_token=raw_attribute
        )

        if raw_attribute is None or (
            type(raw_attribute) is str and not raw_attribute.strip()
        ):
            if optional:
                return None

            raise MissingAPIResponseAttributeError(
                api_resource_url=self._api_resource_url,
                attribute_name=key
            )

        allowed_types = (
            get_args(expected_type)
            if isinstance(expected_type, UnionType)
            else (expected_type,)
        )
        if type(raw_attribute) not in allowed_types:
            raise malformed_exception

        return _parse_attribute(
            raw_attribute,
            malformed_exception,
            parser
        )

def _parse_attribute(
    raw_attribute: Any,
    exception: MalformedAPIResponseAttributeError,
    parser: Callable[[Any], Any] | None = None
) -> Any:
    """
    Calls the given parser function on the given attribute, raising the given
    exception if a ValueParsingError is thrown. Returns the raw attribute if
    the parser is None.
    """
    if parser is not None:
        try:
            parsed_attribute = parser(raw_attribute)
        except ValueParsingError as e:
            raise exception from e
    else:
        parsed_attribute = raw_attribute

    return parsed_attribute
