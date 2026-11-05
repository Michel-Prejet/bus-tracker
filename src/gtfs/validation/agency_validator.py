from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from gtfs.constants.csv_column_headers.agency_headers import AGENCY_NAME_COL_HEADER, AGENCY_URL_COL_HEADER, \
    AGENCY_FARE_URL_COL_HEADER, AGENCY_TIMEZONE_COL_HEADER, AGENCY_LANGUAGE_COL_HEADER, AGENCY_EMAIL_COL_HEADER, \
    AGENCY_PHONE_COL_HEADER
from gtfs.constants.gtfs_constants import AGENCY_FILE_NAME, NUM_AGENCIES_SUPPORTED
from gtfs.domain.agency import Agency
from gtfs.domain.values.email import Email
from gtfs.domain.values.language import Language
from gtfs.domain.values.url import Url
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_row_error import GTFSAttributeError
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.general_validator import validate_and_parse_nonempty_str, validate_and_parse_url, \
    parse_optional_str, validate_and_parse_language_code, validate_and_parse_email
from invariant_helper import require_not_none


def validate_agency_collection(agencies: list[Agency]) -> None:
    """
    Throws an exception if there is not exactly one agency in the given list.

    Note: GTFS supports multiple agencies, but this requires further (intricate)
    implementation details, which are not currently applicable to Winnipeg
    Transit. As such, the number of agencies must be limited to 1 until these
    details are implemented.
    """
    require_not_none(agency_list=agencies)
    for agency in agencies:
        require_not_none(agency_in_list=agency)

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
    require_not_none(raw_agency_name=raw)
    require_valid_row_num(row_num)

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
    require_not_none(raw_agency_url=raw)
    require_valid_row_num(row_num)

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

def validate_and_parse_fare_url(raw: str, row_num: int) -> Url | None:
    """
    Throws an exception if the given string is both non-empty and an invalid
    url; otherwise returns None (if the string is empty) or a URL object
    (if the string is non-empty and a valid URL).
    """
    require_not_none(raw_fare_url=raw)
    require_valid_row_num(row_num)

    url_str = parse_optional_str(raw)
    if url_str is None:
        return None

    try:
        return validate_and_parse_url(url_str)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=AGENCY_FILE_NAME,
            column_name=AGENCY_FARE_URL_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_agency_timezone(raw: str, row_num: int) -> ZoneInfo:
    """
    Throws an exception if the given string is not a valid IANA timezone;
    otherwise returns a ZoneInfo object.
    """
    require_not_none(raw_timezone=raw)
    require_valid_row_num(row_num)

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

def validate_and_parse_agency_language_code(raw: str, row_num: int) -> Language | None:
    """
    Throws an exception if the given string is both non-empty and not a valid
    BCP 47 language tag; returns a Language object otherwise, or None if the
    trimmed string is empty.
    """
    require_not_none(raw_language_code=raw)
    require_valid_row_num(row_num)

    lang_code = parse_optional_str(raw)
    if lang_code is None:
        return None

    try:
        return validate_and_parse_language_code(lang_code)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=AGENCY_FILE_NAME,
            column_name=AGENCY_LANGUAGE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_agency_phone_number(raw: str, row_num: int) -> str | None:
    """
    Returns None if the given string is empty or only whitespace; otherwise
    returns the trimmed string.
    """
    require_not_none(raw_phone_number=raw)
    require_valid_row_num(row_num)

    return parse_optional_str(raw)

def validate_and_parse_agency_email(raw: str, row_num: int) -> Email | None:
    """
    Throws an exception if the given string is both non-empty and an invalid
    email address; returns an Email object otherwise, or None if the given
    string is empty.
    """
    require_not_none(raw_email=raw)
    require_valid_row_num(row_num)

    email_str = parse_optional_str(raw)
    if email_str is None:
        return None

    try:
        return validate_and_parse_email(email_str)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=AGENCY_FILE_NAME,
            column_name=AGENCY_EMAIL_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e
