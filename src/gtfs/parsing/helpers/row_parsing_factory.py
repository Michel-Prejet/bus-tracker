from typing import Callable
from gtfs.exceptions.gtfs_row_error import GTFSAttributeError, GTFSInstanceError, GTFSForeignKeyError
from gtfs.exceptions.domain_error import DomainError
from gtfs.exceptions.value_parsing_error import ValueParsingError
from gtfs.utilities.dict_reader_row_to_csv import dict_reader_row_to_csv


class RowParsingFactory:
    """
    Stores context for a CSV dict reader row, such as the row itself, the row
    number, and the name of file from which it was read. Attributes can then
    be retrieved from the row by specifying a column name and optional
    parser/validator functions; exceptions are thrown where applicable and
    constructed using the row's context.
    """

    def __init__(
            self,
            file_name: str,
            row: dict[str, str | None],
            row_num: int
    ):
        self._file_name = file_name
        self._row = row
        self._row_num = row_num

    def get_attribute[T](
            self,
            column_name: str,
            parser: Callable[[str], T] | None = None,
            validator: Callable[[T], None] | None = None,
            optional: bool = False
    ) -> T | None:
        """
        Retrieves a token from this CSV dict reader row using the given column
        name, then applies the given parser and validation functions, returning
        the resulting token.
        If there is no such column name, or the token retrieved is empty or
        only whitespace, None is returned if the attribute is optional,
        otherwise a GTFSAttributeError is thrown.
        If the parser or validator is None, no parsing and/or validation is
        performed.
        If a ValueParsingError is thrown during parsing or a DomainError is
        thrown during validation, a GTFSAttributeError is thrown.
        """
        raw_token = self._row.get(column_name)

        exception = GTFSAttributeError(
            file_name=self._file_name,
            column_name=column_name,
            row_num=self._row_num,
            invalid_token=raw_token
        )

        if raw_token is None or not raw_token.strip():
            if optional:
                return None

            raise exception

        parsed_token = _parse_attribute(raw_token, exception, parser)

        _validate_attribute(parsed_token, exception, validator)

        return parsed_token

    def get_attribute_as_foreign_key[U](
            self,
            column_name: str,
            referenced_objs: dict[str, U],
            referenced_file_name: str,
            parser: Callable[[str], str] | None = None,
            validator: Callable[[str], None] | None = None,
            optional: bool = False
    ) -> U | None:
        """
        Retrieves a foreign key from the given column in the CSV dict reader,
        then attempts to retrieve the corresponding object from the given list.
        If no such object can be found, throws a GTFSForeignKeyError.
        """
        fk = self.get_attribute(
            column_name=column_name,
            parser=parser,
            validator=validator,
            optional=optional
        )

        if fk is None:
            return None

        referenced_obj = referenced_objs.get(fk)

        if referenced_obj is None:
            raise GTFSForeignKeyError(
                file_name=self._file_name,
                column_name=column_name,
                row_num=self._row_num,
                invalid_token=fk,
                referenced_file_name=referenced_file_name
            )

        return referenced_obj

    def assert_valid_instance(
            self,
            instance_validator: Callable
    ):
        """
        Throws a GTFSInstanceError if the given function throws a DomainError.
        """
        try:
            instance_validator()
        except DomainError as e:
            raise GTFSInstanceError(
                file_name=self._file_name,
                row_num=self._row_num,
                row=dict_reader_row_to_csv(self._row)
            ) from e

def _parse_attribute[T](
        raw_token: str,
        exception: GTFSAttributeError,
        parser: Callable[[str], T] | None = None
) -> T:
    """
    Calls the given parser function on the given token, raising the given
    exception if a ValueParsingError is thrown. Returns the raw token if the
    parser is None.
    """
    if parser is not None:
        try:
            parsed_token = parser(raw_token)
        except ValueParsingError as e:
            raise exception from e
    else:
        parsed_token = raw_token

    return parsed_token

def _validate_attribute[T](
        parsed_token: T,
        exception: GTFSAttributeError,
        validator: Callable[[T], None] | None = None
) -> None:
    """
    Calls the given validator function on the given token, raising the given
    exception if a DomainError is thrown. Takes no action if the validator
    is None.
    """
    if validator is not None:
        try:
            validator(parsed_token)
        except DomainError as e:
            raise exception from e