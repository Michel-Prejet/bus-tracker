"""
Family of exceptions thrown whenever a GTFS file is missing, can't be opened,
or is malformed.
"""

class GTFSFileError(Exception):
    def __init__(self, file_name: str):
        self._file_name = file_name

    @property
    def file_name(self) -> str:
        return self._file_name

class GTFSFileNotFoundError(GTFSFileError):
    pass

class EmptyGTFSFileError(GTFSFileError):
    pass

class GTFSFileColumnError(GTFSFileError):
    def __init__(self, file_name: str, column_name: str):
        super().__init__(file_name)

        self._column_name = column_name

    @property
    def column_name(self) -> str:
        return self._column_name

class MissingGTFSFileColumnError(GTFSFileColumnError):
    pass

class DuplicateGTFSFileColumnError(GTFSFileColumnError):
    pass

class MissingGTFSTokenError(GTFSFileError):
    def __init__(self, file_name: str, column_name: str, row_number: int):
        super().__init__(file_name)

        self._column_name = column_name
        self._row_number = row_number

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def row_number(self) -> int:
        return self._row_number

