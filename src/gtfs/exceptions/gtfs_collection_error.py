from invariant_helper import require_not_none, require_non_empty_str


class GTFSCollectionError(Exception):
    """
    Exception thrown when a collection of objects constructed from a GTFS
    file as a whole violates collection-level domain rules.
    """

    def __init__(self, file_name: str, names_of_columns_with_violated_restrictions: list[str]):
        self._file_name = file_name
        self._violated_column_names = names_of_columns_with_violated_restrictions

        require_not_none(
            file_name=file_name,
            names_of_columns_with_violated_restrictions=self._violated_column_names
        )
        for col in self._violated_column_names:
            require_not_none(column_name_in_list=col)
        require_non_empty_str(file_name=file_name)

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def violated_column_names(self) -> list[str]:
        return self._violated_column_names