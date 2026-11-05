from datetime import date
from gtfs.constants.csv_column_headers.feed_info_headers import PUBLISHER_NAME_COL_HEADER, PUBLISHER_URL_COL_HEADER, \
    FEED_LANGUAGE_COL_HEADER, FEED_START_DATE_COL_HEADER, FEED_END_DATE_COL_HEADER, FEED_EMAIL_COL_HEADER
from gtfs.constants.gtfs_constants import FEED_INFO_FILE_NAME, NUM_FEED_INFOS_ALLOWED, AGENCY_FILE_NAME
from gtfs.domain.feed_info import FeedInfo
from gtfs.domain.values.email import Email
from gtfs.domain.values.language import Language
from gtfs.domain.values.url import Url
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_row_error import GTFSAttributeError, GTFSInstanceError
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.general_validator import validate_and_parse_nonempty_str, validate_and_parse_url, \
    validate_and_parse_language_code, parse_optional_str, validate_and_parse_date, validate_and_parse_email
from invariant_helper import require_not_none


def validate_feed_info_collection(feed_infos: list[FeedInfo]) -> None:
    """
    Throws an exception if there is not exactly one feed info object in the
    given list.
    There must be exactly one feed info as per official GTFS requirements.
    """
    require_not_none(feed_info_list=feed_infos)
    for fi in feed_infos:
        require_not_none(feed_info_in_list=fi)

    if len(feed_infos) != NUM_FEED_INFOS_ALLOWED:
        raise GTFSCollectionError(
            file_name=AGENCY_FILE_NAME,
            names_of_columns_with_violated_restrictions=[
                PUBLISHER_NAME_COL_HEADER, PUBLISHER_URL_COL_HEADER,
                FEED_LANGUAGE_COL_HEADER, FEED_START_DATE_COL_HEADER,
                FEED_END_DATE_COL_HEADER, FEED_EMAIL_COL_HEADER
            ]
        )

def validate_feed_info_attribute_combination(
        start_date: date | None,
        end_date: date | None,
        row: str,
        row_num: int
) -> None:
    """
    Throws an exception if both dates are not None and the start date comes
    after the end date.
    """
    require_not_none(row=row)
    require_valid_row_num(row_num)

    if start_date is not None and end_date is not None:
        if start_date > end_date:
            raise GTFSInstanceError(
                file_name=FEED_INFO_FILE_NAME,
                row=row,
                row_num=row_num
            )

def validate_and_parse_publisher_name(raw: str, row_num: int) -> str:
    """
    Throws an exception if the given string is empty or only whitespace;
    otherwise returns the trimmed string.
    """
    require_not_none(raw_publisher_name=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name = FEED_INFO_FILE_NAME,
            column_name=PUBLISHER_NAME_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_publisher_url(raw: str, row_num: int) -> Url:
    """
    Throws an exception if the given string is not a valid URL; otherwise
    returns a URL object.
    """
    require_not_none(raw_publisher_url=raw)
    require_valid_row_num(row_num)

    try:
        url = validate_and_parse_url(raw)

        if url is None:
            raise ValueError

        return url
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=FEED_INFO_FILE_NAME,
            column_name=PUBLISHER_URL_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_feed_language(raw: str, row_num: int) -> Language:
    """
    Throws an exception if the given string not a valid BCP 47 language tag;
    returns a language object otherwise.
    """
    require_not_none(raw_feed_language=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_language_code(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=FEED_INFO_FILE_NAME,
            column_name=FEED_LANGUAGE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_feed_start_date(raw: str, row_num: int) -> date | None:
    """
    Throws an exception if the given string is both non-empty and not a valid
    date in YYYMMDD format; returns a date object otherwise, or None if the
    given string is empty.
    """
    require_not_none(raw_feed_start_date=raw)
    require_valid_row_num(row_num)

    start_date_str = parse_optional_str(raw)
    if start_date_str is None:
        return None

    try:
        return validate_and_parse_date(start_date_str)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=FEED_INFO_FILE_NAME,
            column_name=FEED_START_DATE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_feed_end_date(raw: str, row_num: int) -> date | None:
    """
    Throws an exception if the given string is both non-empty and not a valid
    date in YYYMMDD format; returns a date object otherwise, or None if the
    given string is empty.
    """
    require_not_none(raw_feed_end_date=raw)
    require_valid_row_num(row_num)

    end_date_str = parse_optional_str(raw)
    if end_date_str is None:
        return None

    try:
        return validate_and_parse_date(end_date_str)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=FEED_INFO_FILE_NAME,
            column_name=FEED_END_DATE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_publisher_email(raw: str, row_num: int) -> Email | None:
    """
    Throws an exception if the given string is both non-empty and an invalid
    email address; returns an Email object otherwise, or None if the given
    string is empty.
    """
    require_not_none(raw_publisher_email=raw)
    require_valid_row_num(row_num)

    email_str = parse_optional_str(raw)
    if email_str is None:
        return None

    try:
        return validate_and_parse_email(email_str)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=FEED_INFO_FILE_NAME,
            column_name=FEED_EMAIL_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

