from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from gtfs.constants.csv_column_headers.agency_headers import AGENCY_NAME_COL_HEADER, AGENCY_URL_COL_HEADER, \
    AGENCY_FARE_URL_COL_HEADER, AGENCY_TIMEZONE_COL_HEADER, AGENCY_LANGUAGE_COL_HEADER, AGENCY_EMAIL_COL_HEADER, \
    AGENCY_PHONE_COL_HEADER
from gtfs.constants.gtfs_constants import AGENCY_FILE_NAME, NUM_AGENCIES_SUPPORTED
from gtfs.domain.agency import Agency
from gtfs.domain.values.url import Url
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_row_error import GTFSAttributeError
from gtfs.validation.general_validator import validate_and_parse_nonempty_str, validate_and_parse_url


def validate_agency_collection(agencies: list[Agency]) -> None:
    """
    Throws an exception if there is not exactly one agency in the given list.
    """
    if len(agencies) != NUM_AGENCIES_SUPPORTED:
        raise GTFSCollectionError(
            file_name=AGENCY_FILE_NAME,
            names_of_columns_with_violated_restrictions=[
                AGENCY_NAME_COL_HEADER, AGENCY_URL_COL_HEADER,
                AGENCY_FARE_URL_COL_HEADER, AGENCY_TIMEZONE_COL_HEADER,
                AGENCY_LANGUAGE_COL_HEADER, AGENCY_EMAIL_COL_HEADER,
                AGENCY_PHONE_COL_HEADER
            ]
        )

def validate_and_parse_agency_name(raw: str, row_num: int) -> str:
    """
    Throws an exception if the given string is empty or only whitespace;
    otherwise returns the trimmed string.
    """
    try:
        return validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=AGENCY_FILE_NAME,
            column_name=AGENCY_NAME_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_agency_url(raw: str, row_num: int) -> Url:
    """
    Throws an exception if the given string is not a valid URL; otherwise
    returns a URL object.
    """
    try:
        url = validate_and_parse_url(raw)

        if url is None:
            raise ValueError

        return url
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=AGENCY_FILE_NAME,
            column_name=AGENCY_URL_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_agency_timezone(raw: str, row_num: int) -> ZoneInfo:
    """
    Throws an exception if the given string is not a valid IANA timezone;
    otherwise returns a ZoneInfo object.
    """
    raw = raw.strip()

    try:
        return ZoneInfo(raw)
    except (ZoneInfoNotFoundError, ValueError) as e:
        raise GTFSAttributeError(
            file_name=AGENCY_FILE_NAME,
            column_name=AGENCY_TIMEZONE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e
