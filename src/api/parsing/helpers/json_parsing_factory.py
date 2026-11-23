from __future__ import annotations
from types import UnionType
from typing import Any, Callable, get_args
from api.exceptions.api_response_error import MissingAPIResponseAttributeError, \
    MalformedAPIResponseAttributeError, IllegalAPIResponseAttributeError, APIAttributeCombinationError
from global_packages.exceptions.domain_error import DomainError
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
        next_level = self._get_attribute(key, optional)
        if next_level is None:
            return None

        if type(next_level) is not dict:
            raise self._get_malformed_exception(key, next_level)

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
        next_level = self._get_attribute(key, optional)
        if next_level is None:
            return None

        if type(next_level) is not list:
            raise self._get_malformed_exception(key, next_level)

        for element in next_level:
            if type(element) is not dict:
                raise self._get_malformed_exception(key, next_level)

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
        validator: Callable[[Any], None] | None = None,
        optional: bool = False
    ) -> Any:
        """
        Returns the value in this dictionary accessed by the given key,
        with the given parser and validators applied. If the value is not of the
        expected type, the parser throws a ValueParsingError, or the validator
        throws a DomainError, an exception is thrown. If the value is None, an
        exception is thrown only if it is not optional, otherwise None is
        returned.
        """
        raw_attribute = self._get_attribute(key, optional)
        if raw_attribute is None:
            return None

        allowed_types = (
            get_args(expected_type)
            if isinstance(expected_type, UnionType)
            else (expected_type,)
        )
        if type(raw_attribute) not in allowed_types:
            raise self._get_malformed_exception(key, raw_attribute)

        parsed_attribute = self._parse_attribute(
            key=key,
            raw_attribute=raw_attribute,
            parser=parser
        )

        self._validate_attribute(
            key=key,
            parsed_attribute=parsed_attribute,
            validator=validator
        )

        return parsed_attribute

    def assert_valid_attribute_combination(
        self,
        validator: Callable,
        attributes: list[Any]
    ) -> None:
        """
        Calls the given validator function with no arguments, and throws an
        exception if a DomainError is thrown.
        """
        try:
            validator()
        except DomainError as e:
            raise APIAttributeCombinationError(
                api_resource_url=self._api_resource_url,
                invalid_attributes=attributes
            ) from e

    def _get_attribute(
        self,
        key: str,
        optional: bool = False
    ) -> Any:
        """
        Retrieves an attribute from the root dictionary using the given
        key. If the attribute is missing and optional, returns None; if it
        is not optional, throws an exception.
        """
        attribute = self._root.get(key)

        if attribute is None or (
                type(attribute) is str and not attribute.strip()
        ):
            if optional:
                return None

            raise MissingAPIResponseAttributeError(
                api_resource_url=self._api_resource_url,
                attribute_name=key
            )

        return attribute

    def _parse_attribute(
        self,
        key: str,
        raw_attribute: Any,
        parser: Callable[[Any], Any] | None = None
    ):
        """
        Calls the given parser function on the given attribute, raising the given
        exception if a ValueParsingError is thrown. Returns the raw attribute if
        the parser is None.
        """
        if parser is not None:
            try:
                parsed_attribute = parser(raw_attribute)
            except ValueParsingError as e:
                raise self._get_malformed_exception(
                    key=key, invalid_token=raw_attribute
                ) from e
        else:
            parsed_attribute = raw_attribute

        return parsed_attribute

    def _validate_attribute(
        self,
        key: str,
        parsed_attribute: Any,
        validator: Callable[[Any], None] | None = None
    ) -> None:
        """
        Calls the given validator function on the given parsed attribute, and
        throws an exception if a DomainError is thrown. Takes no action if the
        given validator is None.
        """
        if validator is not None:
            try:
                validator(parsed_attribute)
            except DomainError as e:
                raise IllegalAPIResponseAttributeError(
                    api_resource_url=self._api_resource_url,
                    attribute_name=key,
                    invalid_token=parsed_attribute
                ) from e

    def _get_malformed_exception(
        self,
        key: str,
        invalid_token: str
    ) -> MalformedAPIResponseAttributeError:
        return MalformedAPIResponseAttributeError(
            api_resource_url=self._api_resource_url,
            attribute_name=key,
            invalid_token=invalid_token
        )
