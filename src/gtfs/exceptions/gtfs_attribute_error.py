from invariant_helper import require_not_none, require_non_empty_str, require_state


class GTFSAttributeError(Exception):
    """
    Exception thrown when an attribute in a CSV row in a GTFS file could not
    be utilized because it is either malformed or violates domain rules.
    """
    def __init__(self, file_name: str, column_name: str, row_num: int, invalid_token: str):
        self._file_name = file_name
        self._column_name = column_name
        self._row_num = row_num
        self._invalid_token = invalid_token

        require_not_none(
            file_name=self._file_name,
            column_name=self._column_name,
            row_number=self._row_num,
            invalid_token=self._invalid_token
        )
        require_non_empty_str(file_name=file_name, column_name=self._column_name)
        require_state(self._row_num >= 1, "Row number should be positive.")

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def column_name(self) -> str:
        return self._column_name
    @property
    def row_num(self) -> int:
        return self._row_num

    @property
    def invalid_token(self) -> str:
        return self._invalid_token