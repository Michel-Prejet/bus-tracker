class GTFSCollectionError(Exception):
    """
    Exception thrown when a collection of objects constructed from a GTFS
    file as a whole violates collection-level domain rules.
    """

    def __init__(self, file_name: str, names_of_columns_with_violated_restrictions: list[str]):
        self._file_name = file_name
        self._violated_column_names = names_of_columns_with_violated_restrictions

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def violated_column_names(self) -> list[str]:
        return self._violated_column_names