from gtfs.exceptions.csv_parsing.gtfs_file_error import GTFSFileError, GTFSFileNotFoundError, EmptyGTFSFileError, \
    MissingGTFSTokenError, MissingGTFSFileColumnError, DuplicateGTFSFileColumnError, GTFSFileColumnError
from gtfs.exceptions.domain_validation.route_error import RouteError, EmptyRouteIdError, InvalidRouteTypeError, \
    InvalidRouteUrlError, RouteAttributeError, InvalidRouteBackgroundColourError, InvalidRouteTextColourError, \
    InvalidRouteSortOrderError, DuplicateRouteIdError, MissingRouteNameError


def get_err_msg(e: Exception) -> str:
    """
    Returns the error message associated with the given exception type.
    """
    match e:
        case GTFSFileError():
            return _get_err_msg_for_gtfs_file_error(e)
        case RouteError():
            return _get_err_msg_for_route_error(e)

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

def _get_err_msg_for_route_error(e: RouteError) -> str:
    match e:
        case RouteAttributeError():
            PREFIX = f"Failed to create route from row {e.row_num} because"

            match e:
                case EmptyRouteIdError():
                    return f"{PREFIX} the route ID is empty."
                case InvalidRouteTypeError():
                    return f"{PREFIX} the route type is invalid."
                case InvalidRouteUrlError():
                    return f"{PREFIX} the route URL is invalid."
                case InvalidRouteBackgroundColourError():
                    return f"{PREFIX} the route background colour is invalid."
                case InvalidRouteTextColourError():
                    return f"{PREFIX} the route text colour is invalid."
                case InvalidRouteSortOrderError():
                    return f"{PREFIX} the route sort order is invalid."
                case MissingRouteNameError():
                    return f"{PREFIX} both route names are missing."
                case RouteAttributeError():
                    return f"{PREFIX} of an unspecified attribute error."
        case DuplicateRouteIdError():
            return (f"Failed to create routes from the CSV file because route "
                    f"ID {e.duplicated_route_id} is duplicated.")

    return f"Failed to create routes from the CSV file because of an unspecified error."
