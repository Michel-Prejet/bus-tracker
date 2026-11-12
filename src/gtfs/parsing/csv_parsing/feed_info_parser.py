from gtfs.constants.csv_column_headers.feed_info_headers import PUBLISHER_NAME_COL_HEADER, PUBLISHER_URL_COL_HEADER, \
    FEED_LANGUAGE_COL_HEADER, FEED_START_DATE_COL_HEADER, FEED_END_DATE_COL_HEADER
from gtfs.constants.gtfs_constants import FEED_INFO_FILE_NAME
from gtfs.parsing.helpers.gtfs_file_parser import parse_gtfs_file
from gtfs.domain.feed_info import FeedInfo
from gtfs.parsing.helpers.row_parsing_factory import RowParsingFactory
from gtfs.parsing.validation.instance_validator import assert_not_greater_than
from gtfs.parsing.value_parsing.datetime_parser import parse_date
from gtfs.parsing.value_parsing.primitive_parser import parse_string
from gtfs.parsing.value_parsing.url_parser import parse_url
from gtfs.parsing.validation.collection_validator import validate_feed_infos


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
        collection_validator=validate_feed_infos
    )[0]

def _create_feed_info_from_row(row: dict[str, str | None], row_num: int) -> FeedInfo:
    parser = RowParsingFactory(
        file_name=FEED_INFO_FILE_NAME,
        row=row,
        row_num=row_num
    )

    publisher_name = parser.get_attribute(
        column_name=PUBLISHER_NAME_COL_HEADER,
        parser=parse_string
    )

    publisher_url = parser.get_attribute(
        column_name=PUBLISHER_URL_COL_HEADER,
        parser=parse_url
    )

    start_date = parser.get_attribute(
        column_name=FEED_START_DATE_COL_HEADER,
        parser=parse_date,
        optional=True
    )

    end_date = parser.get_attribute(
        column_name=FEED_END_DATE_COL_HEADER,
        parser=parse_date,
        optional=True
    )

    parser.assert_valid_instance(
        lambda: assert_not_greater_than(start_date, end_date)
    )

    return FeedInfo(
        publisher_name=publisher_name,
        publisher_url=publisher_url,
        start_date=start_date,
        end_date=end_date
    )