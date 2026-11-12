from gtfs.constants.csv_column_headers.service_pattern_headers import SERVICE_ID_COL_HEADER, \
    SERVICE_PATTERN_START_DATE_COL_HEADER, SERVICE_PATTERN_END_DATE_COL_HEADER, MONDAY_COL_HEADER, TUESDAY_COL_HEADER, \
    WEDNESDAY_COL_HEADER, THURSDAY_COL_HEADER, FRIDAY_COL_HEADER, SATURDAY_COL_HEADER, SUNDAY_COL_HEADER
from gtfs.constants.gtfs_constants import SERVICE_PATTERNS_FILE_NAME
from gtfs.domain.enums.day_of_week import DayOfWeek
from gtfs.domain.values.date_range import DateRange
from gtfs.parsing.helpers.gtfs_file_parser import parse_gtfs_file
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.parsing.helpers.row_parsing_factory import RowParsingFactory
from gtfs.parsing.validation.instance_validator import assert_not_greater_than
from gtfs.parsing.value_parsing.datetime_parser import parse_date
from gtfs.parsing.value_parsing.primitive_parser import parse_string, parse_bool
from gtfs.parsing.validation.collection_validator import validate_service_patterns


SERVICE_PATTERN_REQUIRED_COLUMNS = [
    SERVICE_ID_COL_HEADER,
    MONDAY_COL_HEADER,
    TUESDAY_COL_HEADER,
    WEDNESDAY_COL_HEADER,
    THURSDAY_COL_HEADER,
    FRIDAY_COL_HEADER,
    SATURDAY_COL_HEADER,
    SUNDAY_COL_HEADER,
    SERVICE_PATTERN_START_DATE_COL_HEADER,
    SERVICE_PATTERN_END_DATE_COL_HEADER
]

def parse_service_patterns(file_name: str) -> dict[str, ServicePattern]:
    """
    Creates a dictionary of ServicePattern objects (keyed by service ID) from
    the rows in the given file, or throws an exception if the file or its
    contents are invalid.
    """
    patterns = parse_gtfs_file(
        file_name=file_name,
        required_column_names=SERVICE_PATTERN_REQUIRED_COLUMNS,
        object_builder_from_row=_create_service_pattern_from_row,
        collection_validator=validate_service_patterns
    )

    return {pattern.service_id: pattern for pattern in patterns}

def _create_service_pattern_from_row(row: dict[str, str],
                                     row_num: int) -> ServicePattern:
    parser = RowParsingFactory(
        file_name=SERVICE_PATTERNS_FILE_NAME,
        row=row,
        row_num=row_num
    )

    service_id = parser.get_attribute(
        column_name=SERVICE_ID_COL_HEADER,
        parser=parse_string
    )

    start_date = parser.get_attribute(
        column_name=SERVICE_PATTERN_START_DATE_COL_HEADER,
        parser=parse_date
    )
    end_date = parser.get_attribute(
        column_name=SERVICE_PATTERN_END_DATE_COL_HEADER,
        parser=parse_date
    )
    parser.assert_valid_instance(
        lambda: assert_not_greater_than(start_date, end_date)
    )

    include_monday = parser.get_attribute(
        column_name=MONDAY_COL_HEADER,
        parser=parse_bool
    )
    include_tuesday = parser.get_attribute(
        column_name=TUESDAY_COL_HEADER,
        parser=parse_bool
    )
    include_wednesday = parser.get_attribute(
        column_name=WEDNESDAY_COL_HEADER,
        parser=parse_bool
    )
    include_thursday = parser.get_attribute(
        column_name=THURSDAY_COL_HEADER,
        parser=parse_bool
    )
    include_friday = parser.get_attribute(
        column_name=FRIDAY_COL_HEADER,
        parser=parse_bool
    )
    include_saturday = parser.get_attribute(
        column_name=SATURDAY_COL_HEADER,
        parser=parse_bool
    )
    include_sunday = parser.get_attribute(
        column_name=SUNDAY_COL_HEADER,
        parser=parse_bool
    )

    active_weekdays = [
        day
        for day, include in [
            (DayOfWeek.MONDAY, include_monday),
            (DayOfWeek.TUESDAY, include_tuesday),
            (DayOfWeek.WEDNESDAY, include_wednesday),
            (DayOfWeek.THURSDAY, include_thursday),
            (DayOfWeek.FRIDAY, include_friday),
            (DayOfWeek.SATURDAY, include_saturday),
            (DayOfWeek.SUNDAY, include_sunday)
        ]
        if include
    ]

    return ServicePattern(
        service_id,
        set(active_weekdays),
        DateRange(start_date, end_date)
    )
