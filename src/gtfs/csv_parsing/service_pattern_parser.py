from gtfs.constants.csv_column_headers.service_pattern_headers import SERVICE_ID_COL_HEADER, \
    SERVICE_PATTERN_START_DATE_COL_HEADER, SERVICE_PATTERN_END_DATE_COL_HEADER, MONDAY_COL_HEADER, TUESDAY_COL_HEADER, \
    WEDNESDAY_COL_HEADER, THURSDAY_COL_HEADER, FRIDAY_COL_HEADER, SATURDAY_COL_HEADER, SUNDAY_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import parse_gtfs_file
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.service_pattern_validator import validate_and_parse_service_id, validate_and_parse_start_date, \
    validate_and_parse_end_date, validate_and_parse_active_weekdays, validate_service_pattern_collection, \
    validate_and_parse_service_pattern_date_range
from invariant_helper import require_not_none


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

def parse_service_patterns(file_name: str) -> list[ServicePattern]:
    """
    Creates a list of ServicePattern objects from the rows in the given file,
    or throws an exception if the file or its content are invalid.
    """
    return parse_gtfs_file(
        file_name=file_name,
        required_column_names=SERVICE_PATTERN_REQUIRED_COLUMNS,
        object_builder_from_row=_create_service_pattern_from_row,
        collection_validator=validate_service_pattern_collection
    )

def _create_service_pattern_from_row(row: dict[str, str],
                                     row_num: int) -> ServicePattern:
    require_not_none(row=row)
    require_valid_row_num(row_num)

    service_id = validate_and_parse_service_id(row[SERVICE_ID_COL_HEADER], row_num)

    start_date = validate_and_parse_start_date(
        row[SERVICE_PATTERN_START_DATE_COL_HEADER],
        row_num
    )
    end_date = validate_and_parse_end_date(
        row[SERVICE_PATTERN_END_DATE_COL_HEADER],
        row_num
    )
    date_range = validate_and_parse_service_pattern_date_range(
        start_date,
        end_date,
        row_num
    )

    active_weekdays = validate_and_parse_active_weekdays(
        {
            "MONDAY": row[MONDAY_COL_HEADER],
            "TUESDAY": row[TUESDAY_COL_HEADER],
            "WEDNESDAY": row[WEDNESDAY_COL_HEADER],
            "THURSDAY": row[THURSDAY_COL_HEADER],
            "FRIDAY": row[FRIDAY_COL_HEADER],
            "SATURDAY": row[SATURDAY_COL_HEADER],
            "SUNDAY": row[SUNDAY_COL_HEADER]
        },
        row_num
    )

    return ServicePattern(service_id, active_weekdays, date_range)
