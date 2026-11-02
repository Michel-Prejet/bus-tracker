from gtfs.utilities.require_valid_row_num import require_valid_row_num
from invariant_helper import require_not_none, require_non_empty_str


class GTFSRowError(Exception):
    """
    Exception thrown when a row in a GTFS file is invalid. This includes rows
    with malformed attributes or attributes outside the permitted domain,
    attributes or combinations of attributes that are illogical or violate GTFS
    guidelines, or invalid foreign keys.
    """
    def __init__(self, file_name: str, row_num: int):
        self._file_name = file_name
        self._row_num = row_num

        require_not_none(file_name=file_name)
        require_non_empty_str(file_name=file_name)
        require_valid_row_num(row_num)

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def row_num(self) -> int:
        return self._row_num

class GTFSAttributeError(GTFSRowError):
    """
    Exception thrown when an attribute in a row is malformed, or falls outside
    the set of permitted values.
    Only applicable to single attributes within the row and their respective
    domain. Should not be thrown based on relationships between attributes.
    """
    def __init__(self, file_name: str, row_num: int,
                 column_name: str, invalid_token: str) -> None:
        super().__init__(file_name, row_num)

        self._column_name = column_name
        self._invalid_token = invalid_token

        require_not_none(column_name=column_name, invalid_token=invalid_token)
        require_non_empty_str(column_name=column_name)

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def invalid_token(self) -> str:
        return self._invalid_token

class GTFSLogicError(GTFSRowError):
    """
    Exception thrown when a combination of attributes in a row violates
    basic logic (e.g. a start date that comes after an end date).
    """
    def __init__(self, file_name: str, row_num: int,
                 col_names_and_invalid_tokens: dict[str, str]) -> None:
        super().__init__(file_name, row_num)

        self._col_names_and_invalid_tokens = col_names_and_invalid_tokens

        require_not_none(
            dictionary_of_column_names_and_invalid_tokens=col_names_and_invalid_tokens
        )
        for col, token in col_names_and_invalid_tokens.items():
            require_not_none(column_in_dictionary=col, token_in_dictionary=token)
            require_non_empty_str(column_in_dictionary=col)

    @property
    def col_names_and_invalid_tokens(self) -> dict[str, str]:
        return self._col_names_and_invalid_tokens

class GTFSInstanceError(GTFSRowError):
    """
    Exception thrown when a row violates official GTFS rules imposed on that
    object type.
    Only applicable to instances, not collections.
    """
    def __init__(self, file_name: str, row_num: int, row: str) -> None:
        super().__init__(file_name, row_num)

        self._row = row

        require_not_none(row=row)

    @property
    def row(self) -> str:
        return self._row

class GTFSForeignKeyError(GTFSAttributeError):
    """
    Exception thrown when a foreign key in a row does not correspond to
    any row in the referenced file.
    """
    def __init__(self, file_name: str, row_num: int,
                 column_name: str, invalid_token: str,
                 referenced_file_name: str) -> None:
        super().__init__(file_name, row_num, column_name, invalid_token)

        self._referenced_file_name = referenced_file_name

        require_not_none(referenced_file_name=referenced_file_name)
        require_non_empty_str(referenced_file_name=referenced_file_name)

    @property
    def referenced_file_name(self) -> str:
        return self._referenced_file_name