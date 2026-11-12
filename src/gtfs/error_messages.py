from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_file_error import GTFSFileError, GTFSFileNotFoundError, EmptyGTFSFileError, \
    MissingGTFSTokenError, MissingGTFSFileColumnError, DuplicateGTFSFileColumnError, GTFSFileColumnError
from gtfs.exceptions.gtfs_row_error import GTFSRowError, GTFSAttributeError, GTFSInstanceError, \
    GTFSForeignKeyError


def get_err_msg(e: Exception) -> str:
    """
    Returns the error message associated with the given exception type.
    """
    from gtfs.exceptions.gtfs_row_error import GTFSRowError
    match e:
        case GTFSFileError():
            return _get_err_msg_for_gtfs_file_error(e)
        case GTFSRowError():
            return _get_err_msg_for_gtfs_row_error(e)
        case GTFSCollectionError():
            return (
                f"Could not finish parsing '{e.file_name}' because the "
                f"collection of objects constructed violates business rules "
                f"associated with the file.\n"
                f"Problematic values could be found in the column(s): "
                f"{", ".join(map(str, e.violated_column_names))}."
            )

    return f"An unexpected error occurred: {e}"

def _get_err_msg_for_gtfs_file_error(e: GTFSFileError) -> str:
    match e:
        case GTFSFileNotFoundError():
            return f"The GTFS file '{e.file_name}' could not be opened."
        case EmptyGTFSFileError():
            return f"The GTFS file '{e.file_name}' is empty."
        case MissingGTFSTokenError():
            return f"The token '{e.column_name}' on row {e.row_number} of '{e.file_name}' is missing."
        case MissingGTFSFileColumnError():
            return f"The column '{e.column_name}' is missing in '{e.file_name}'."
        case DuplicateGTFSFileColumnError():
            return f"The column '{e.column_name}' is duplicated in '{e.file_name}'."
        case GTFSFileColumnError():
            return f"The column '{e.column_name}' in the file '{e.file_name}' caused an unspecified error."

    return f"The file '{e.file_name}' caused an unspecified error."

def _get_err_msg_for_gtfs_row_error(e: GTFSRowError) -> str:
    match e:
        case GTFSForeignKeyError():
            return (
                f"Object construction failed on row {e.row_num} of "
                f"'{e.file_name}' because the foreign key '{e.invalid_token}' "
                f"in the column '{e.column_name}' does not correspond to any "
                f"row in '{e.referenced_file_name}'."
            )
        case GTFSAttributeError():
            return (
                f"Object construction failed on row {e.row_num} of "
                f"'{e.file_name}' due to the invalid token '{e.invalid_token}' "
                f"in column '{e.column_name}'."
            )
        case GTFSInstanceError():
            return (
                f"Object construction failed on row {e.row_num} of "
                f"'{e.file_name}' due to the invalid instance given by the row:\n"
                f"{e.row}"
            )

    return f"Row {e.row_num} in '{e.file_name}' caused an unspecified error."
