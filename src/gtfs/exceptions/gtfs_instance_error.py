from gtfs.utilities.require_valid_row_num import require_valid_row_num
from invariant_helper import require_not_none, require_non_empty_str


class GTFSInstanceError(Exception):
    """
    Exception thrown when a CSV row in a GTFS file corresponds to an invalid
    instance of an object.
    """
    def __init__(self, file_name: str, row: str, row_num: int):
        self._file_name = file_name
        self._row = row
        self._row_num = row_num

        require_not_none(
            file_name=file_name,
            row=self._row
        )
        require_non_empty_str(file_name=file_name)
        require_valid_row_num(row_num)

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def row(self):
        return self._row

    @property
    def row_num(self):
        return self._row_num