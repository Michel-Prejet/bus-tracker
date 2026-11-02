from gtfs.constants.csv_column_headers.stop_headers import STOP_ID_COL_HEADER, STOP_NAME_COL_HEADER, \
    STOP_LATITUDE_COL_HEADER, STOP_LONGITUDE_COL_HEADER, STOP_URL_COL_HEADER
from gtfs.constants.gtfs_constants import STOPS_FILE_NAME
from gtfs.domain.stop import Stop
from gtfs.domain.values.url import Url
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_row_error import GTFSAttributeError
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.general_validator import parse_optional_str, validate_and_parse_latitude, \
    validate_and_parse_longitude, validate_and_parse_url, validate_and_parse_nonempty_str, assert_that_ids_are_unique
from invariant_helper import require_not_none


def validate_stop_collection(stops: list[Stop]) -> None:
    """
    Throws an exception if the same stop ID appears more than once in the
    list of stops.
    """
    require_not_none(stop_list=stops)
    for stop in stops:
        require_not_none(stop_in_list=stop)

    try:
        assert_that_ids_are_unique([stop.id for stop in stops])
    except ValueError:
        raise GTFSCollectionError(
            file_name=STOPS_FILE_NAME,
            names_of_columns_with_violated_restrictions=[STOP_ID_COL_HEADER]
        )

def validate_and_parse_stop_id(raw: str, row_num: int) -> str:
    """
    Throws an exception if the given string is empty or only whitespace.
    Otherwise, the trimmed string is returned.
    """
    require_not_none(raw_stop_id=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=STOPS_FILE_NAME,
            column_name=STOP_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_stop_code(raw: str, row_num: int) -> str | None:
    """
    Returns None if the given string is empty or only whitespace; otherwise
    returns the trimmed string.
    """
    require_not_none(raw_stop_code=raw)
    require_valid_row_num(row_num)

    return parse_optional_str(raw)

def validate_and_parse_stop_name(raw: str, row_num: int) -> str:
    """
    Throws an exception if the given string is empty or only whitespace; returns
    the trimmed string otherwise.
    """
    require_not_none(raw_stop_name=raw)
    require_valid_row_num(row_num)

    raw = raw.strip()

    if not raw:
        raise GTFSAttributeError(
            file_name=STOPS_FILE_NAME,
            column_name=STOP_NAME_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        )

    return raw

def validate_and_parse_stop_latitude(raw: str, row_num: int) -> float:
    """
    Throws an exception if the given string is not a floating-point value between
    -90 and 90 (inclusive); returns a float otherwise.
    """
    require_not_none(raw_latitude=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_latitude(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=STOPS_FILE_NAME,
            column_name=STOP_LATITUDE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_stop_longitude(raw: str, row_num: int) -> float:
    """
    Throws an exception if the given string is not a floating-point value between
    -180 and 180 (inclusive); returns a float otherwise.
    """
    require_not_none(raw_longitude=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_longitude(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=STOPS_FILE_NAME,
            column_name=STOP_LONGITUDE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_stop_url(raw: str, row_num: int) -> Url | None:
    """
    Throws an exception if the given string is not a valid URL; otherwise
    returns the corresponding Url object.
    """
    require_not_none(raw_stop_url=raw)
    require_valid_row_num(row_num)

    raw = raw.strip()

    if not raw:
        return None

    try:
        return validate_and_parse_url(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=STOPS_FILE_NAME,
            column_name=STOP_URL_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

