from gtfs.constants.csv_column_headers.feed_info_headers import PUBLISHER_NAME_COL_HEADER, PUBLISHER_URL_COL_HEADER, \
    FEED_LANGUAGE_COL_HEADER, FEED_START_DATE_COL_HEADER, FEED_END_DATE_COL_HEADER, FEED_EMAIL_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import get_opt_attribute, parse_gtfs_file
from gtfs.domain.feed_info import FeedInfo
from gtfs.utilities.dict_reader_row_to_csv import dict_reader_row_to_csv
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.feed_info_validator import validate_and_parse_publisher_name, validate_and_parse_publisher_url, \
    validate_and_parse_feed_language, validate_and_parse_feed_start_date, validate_and_parse_feed_end_date, \
    validate_and_parse_publisher_email, validate_feed_info_attribute_combination, validate_feed_info_collection
from invariant_helper import require_not_none


FEED_INFO_REQUIRED_COLUMNS = [
    PUBLISHER_NAME_COL_HEADER,
    PUBLISHER_URL_COL_HEADER,
    FEED_LANGUAGE_COL_HEADER
]

def parse_feed_info(file_name: str) -> FeedInfo:
    """
    Creates a feed info object from the row in the given file, or throws an
    exception if the file or its contents are invalid.
    """
    return parse_gtfs_file(
        file_name=file_name,
        required_column_names=FEED_INFO_REQUIRED_COLUMNS,
        object_builder_from_row=_create_feed_info_from_row,
        collection_validator=validate_feed_info_collection
    )[0]

def _create_feed_info_from_row(row: dict[str, str | None], row_num: int) -> FeedInfo:
    require_not_none(row=row)
    require_valid_row_num(row_num)

    publisher_name = validate_and_parse_publisher_name(
        row[PUBLISHER_NAME_COL_HEADER],
        row_num
    )

    publisher_url = validate_and_parse_publisher_url(
        row[PUBLISHER_URL_COL_HEADER],
        row_num
    )

    feed_language = validate_and_parse_feed_language(
        row[FEED_LANGUAGE_COL_HEADER],
        row_num
    )

    start_date = get_opt_attribute(
        column_name=FEED_START_DATE_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_feed_start_date
    )

    end_date = get_opt_attribute(
        column_name=FEED_END_DATE_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_feed_end_date
    )

    contact_email = get_opt_attribute(
        column_name=FEED_EMAIL_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_publisher_email
    )

    validate_feed_info_attribute_combination(
        start_date, end_date,
        dict_reader_row_to_csv(row),
        row_num
    )

    return FeedInfo(
        publisher_name=publisher_name,
        publisher_url=publisher_url,
        language=feed_language,
        start_date=start_date,
        end_date=end_date,
        contact_email=contact_email
    )