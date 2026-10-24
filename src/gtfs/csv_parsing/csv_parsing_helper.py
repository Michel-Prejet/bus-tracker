from typing import Callable
from gtfs.exceptions.gtfs_file_error import MissingGTFSTokenError
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.gtfs_file_opener import GTFSFileOpener
from invariant_helper import require_not_none, require_non_empty_str, require_state


def parse_gtfs_file[T](
        file_name: str,
        required_column_names: list[str],
        object_builder_from_row: Callable[[dict[str, str | None], int], T],
        collection_validator: Callable[[list[T]], None] | None = None
) -> list[T]:
    """
    Parses the GTFS file with the given name. Converts CSV rows in the file
    into objects of the given generic type. Throws exceptions if the file
    structure or the contents of the rows are invalid.
    """
    require_not_none(
        file_name=file_name,
        list_of_required_column_names=required_column_names,
        object_builder_function=object_builder_from_row
    )
    require_non_empty_str(file_name=file_name)

    objects: list[T] = []

    with GTFSFileOpener(file_name, required_column_names) as file:
        reader = file.reader

        for row in reader:
            assert_no_missing_tokens_in_row(row, file_name, reader.line_num)

            obj = object_builder_from_row(row, reader.line_num)
            objects.append(obj)

        if collection_validator is not None:
            collection_validator(objects)

        return objects

def get_opt_attribute[T](
        column_name: str,
        row: dict[str, str],
        row_num: int,
        validator: Callable[[str, int], T]
) -> T | None:
    """
    Returns the parsed attribute in the given column of the given row,
    or None if the column doesn't exist. Exceptions may be thrown on
    invalid inputs when calling the validator.
    """
    require_not_none(
        column_name=column_name,
        row=row,
        row_number=row_num,
        validator=validator
    )
    require_non_empty_str(column_name=column_name)
    require_valid_row_num(row_num)

    token_raw = row.get(column_name)

    if token_raw is None:
        return None

    return validator(token_raw, row_num)

def assert_no_missing_tokens_in_row(
        row: dict[str, str | None],
        file_name: str,
        row_number: int
) -> None:
    """
    Throws an exception if any of the values in the given dictionary are None.
    """
    require_not_none(
        row=row,
        file_name=file_name
    )
    require_non_empty_str(file_name=file_name)

    for column_name, value in row.items():
        if value is None:
            raise MissingGTFSTokenError(file_name, column_name, row_number)