from invariant_helper import require_non_empty_str, require_not_none


class GTFSForeignKeyError(Exception):
    """
    Exception thrown when a foreign key in a GTFS file does not reference
    an existing row.
    """
    def __init__(self, file_name: str, column_name: str, invalid_token: str):
        self._file_name = file_name
        self._column_name = column_name
        self._invalid_token = invalid_token

        require_not_none(
            file_name=self._file_name,
            column_name=self._column_name,
            invalid_token=self._invalid_token
        )
        require_non_empty_str(file_name=file_name, column_name=self._column_name)

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def invalid_token(self) -> str:
        return self._invalid_token