import csv
from typing import TextIO, Sequence
from gtfs.exceptions.csv_parsing.gtfs_file_error import GTFSFileNotFoundError, MissingGTFSFileColumnError, \
    DuplicateGTFSFileColumnError, EmptyGTFSFileError
from gtfs.gtfs_constants import FILE_ENCODING
from utilities.invariant_helper import require_not_none, require_non_empty_str, require_state


class GTFSFileOpener:
    """
    Context manager for GTFS CSV files. When invoked, checks that the file
    can be opened and has a valid header.
    """

    def __init__(self, file_name: str, required_column_names: list[str]):
        self._file_name = file_name
        self._required_column_names = required_column_names
        self._file: TextIO | None = None
        self._reader: csv.DictReader | None = None

        self._check_gtfs_file_opener()

    def __enter__(self) -> "GTFSFileOpener":
        try:
            self._file = self._attempt_open_file()
            self._reader = csv.DictReader(self._file, delimiter=",")

            self._validate_header()

            return self
        except Exception:
            self._close()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._close()

    @property
    def reader(self) -> csv.DictReader:
        require_state(
            self._reader is not None,
            "DictReader should never be None by the time it is accessed publicly."
        )

        return self._reader

    def _attempt_open_file(self) -> TextIO:
        """
        Returns the file with the stored file name, or raises an exception if
        it could not be opened.
        """
        try:
            return open(self._file_name, encoding=FILE_ENCODING, newline="")
        except FileNotFoundError:
            raise GTFSFileNotFoundError(self._file_name)

    def _validate_header(self) -> None:
        """
        Raises an exception if there are missing or duplicate column names
        in the header.
        """
        require_state(
            self._reader is not None,
            "Reader should have been initialized before validating the header."
        )

        column_names = self._reader.fieldnames

        if column_names is None:
            raise EmptyGTFSFileError(self._file_name)

        self._assert_required_column_names_present(column_names)

        self._assert_column_names_not_duplicated(column_names)

    def _assert_required_column_names_present(self, column_names: Sequence[str]) -> None:
        require_not_none(column_names_to_validate=column_names)

        for column_name in self._required_column_names:
            if column_name not in column_names:
                raise MissingGTFSFileColumnError(self._file_name, column_name)

    def _assert_column_names_not_duplicated(self, column_names: Sequence[str]) -> None:
        require_not_none(column_names_to_validate=column_names)

        column_names_seen = set()

        for column_name in column_names:
            if column_name in column_names_seen:
                raise DuplicateGTFSFileColumnError(self._file_name, column_name)

            column_names_seen.add(column_name)

    def _close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None

        self._reader = None

    def _check_gtfs_file_opener(self) -> None:
        require_not_none(
            gtfs_file_name=self._file_name,
            required_column_names=self._required_column_names
        )

        require_non_empty_str(gtfs_file_name=self._file_name)

        for col in self._required_column_names:
            require_not_none(column_name_in_list=col)
            require_non_empty_str(column_name_in_list=col)

