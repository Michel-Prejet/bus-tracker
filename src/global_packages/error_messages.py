import psycopg
from api.exceptions.api_request_error import APIRequestError, APITimeoutError, APIConnectionError, APIJsonError, \
    APIRedirectError, BadAPIRequestError, APIKeyError, APIAccessError, APIResourceNotFoundError, \
    TooManyAPIRequestsError, APIHTTPError
from api.exceptions.api_response_error import APIResponseAttributeError, MissingAPIResponseAttributeError, \
    MalformedAPIResponseAttributeError, IllegalAPIResponseAttributeError, APIResponseError, APIAttributeCombinationError
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_file_error import GTFSFileError, GTFSFileNotFoundError, EmptyGTFSFileError, \
    MissingGTFSTokenError, MissingGTFSFileColumnError, DuplicateGTFSFileColumnError, GTFSFileColumnError
from gtfs.exceptions.gtfs_row_error import GTFSRowError, GTFSAttributeError, GTFSInstanceError, \
    GTFSForeignKeyError


def get_err_msg(e: Exception) -> str:
    """
    Returns the error message associated with the given exception type.
    """
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
                f"{_format_str_list(e.violated_column_names)}."
            )
        case psycopg.Error():
            return _get_err_msg_for_db_write_error(e)
        case APIResponseAttributeError():
            return _get_err_msg_for_api_response_error(e)
        case APIRequestError():
            return _get_err_msg_for_api_request_error(e)

    return f"An unexpected error occurred ({type(e).__name__}): {e}"

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

def _get_err_msg_for_db_write_error(e: psycopg.Error) -> str:
    match e:
        case psycopg.IntegrityError():
            return f"Database integrity constraint violated: {e}"
        case psycopg.OperationalError():
            return f"Database operation failed: {e}"
        case psycopg.ProgrammingError():
            return f"Database SQL error: {e}"
        case psycopg.DatabaseError():
            return f"Database error: {e}"

    return f"PostgreSQL client error: {e}"

def _get_err_msg_for_api_response_error(e: APIResponseError) -> str:
    match e:
        case MissingAPIResponseAttributeError():
            return (
                f"Could not finish parsing API response from "
                f"'{e.api_resource_url}' because the attribute "
                f"'{e.attribute_name}' was missing."
            )
        case MalformedAPIResponseAttributeError():
            return (
                f"Could not finish parsing API response from "
                f"'{e.api_resource_url}' because the value "
                f"'{e.invalid_token}' provided for the attribute "
                f"'{e.attribute_name}' is malformed and could not be "
                f"parsed as the expected type."
            )
        case IllegalAPIResponseAttributeError():
            return (
                f"Could not finish parsing API response from "
                f"'{e.api_resource_url}' because the value "
                f"{e.invalid_token} provided for the attribute "
                f"'{e.attribute_name}' violates business logic."
            )
        case APIAttributeCombinationError():
            return (
                f"Could not finish parsing API response from "
                f"'{e.api_resource_url}' because the following "
                f"combination of attributes violates business logic: "
                f"\n{_format_str_list(e.invalid_attributes)}."
            )
        case APIResponseAttributeError():
            return (
                f"Could finish parsing API response from '{e.api_resource_url}' "
                f"due to an unspecified error with the attribute '{e.attribute_name}'."
            )

    return (
        f"Could finish parsing API response from '{e.api_resource_url}' "
        f"due to an unspecified error."
    )

def _get_err_msg_for_api_request_error(e: APIRequestError) -> str:
    match e:
        case APITimeoutError():
            return f"The API request '{e.api_resource_url}' timed out."
        case APIConnectionError():
            return (
                f"Could not establish a connection to the API through the "
                f"request '{e.api_resource_url}'."
            )
        case APIJsonError():
            return (
                f"The API request '{e.api_resource_url}' could not be "
                f"parsed as a JSON dictionary.'"
            )
        case APIRedirectError():
            return (
                f"The API request '{e.api_resource_url}' resulted in too many "
                f"server redirects.'"
            )
        case BadAPIRequestError():
            return (
                f"The API request '{e.api_resource_url}' was rejected because "
                f"it was invalid (HTTP {e.http_status})."
            )
        case APIKeyError():
            return (
                f"The API request '{e.api_resource_url}' was rejected because "
                f"the API key is missing or invalid (HTTP {e.http_status})."
            )
        case APIAccessError():
            return (
                f"The API request '{e.api_resource_url}' was rejected because "
                f"the requested resource was denied (HTTP {e.http_status})."
            )
        case APIResourceNotFoundError():
            return (
                f"The API request '{e.api_resource_url}' was rejected because "
                f"the requested resource could not be found (HTTP {e.http_status})."
            )
        case TooManyAPIRequestsError():
            return (
                f"The API request '{e.api_resource_url}' was rejected because "
                f"the request limit has been exceeded (HTTP {e.http_status})."
            )
        case APIHTTPError():
            return (
                f"The API request '{e.api_resource_url}' failed due to an "
                f"HTTP {e.http_status} error."
            )

    return f"An unspecified error occurred with the API request '{e.api_resource_url}'."

def _format_str_list(values: list[str]) -> str:
    """
    Returns all the strings in the given list as a single comma-separated string,
    in which each value is in single quotes.
    """
    num_strings = len(values)

    result = ""
    for i in range(num_strings - 1):
        result += f"'{values[i]}', "

    if num_strings > 0:
        result += f"'{values[num_strings- 1]}'"

    return result

