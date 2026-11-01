from gtfs.constants.csv_column_headers.service_pattern_override_headers import OVERRIDE_SERVICE_ID_COL_HEADER, \
    OVERRIDE_DATE_COL_HEADER, OVERRIDE_TYPE_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import parse_gtfs_file
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.service_pattern.service_pattern_override import ServicePatternOverride
from gtfs.validation.service_pattern_override_validator import validate_and_parse_override_service_id, \
    validate_and_parse_override_date, validate_and_parse_override_type, get_service_pattern_from_foreign_key, \
    validate_service_pattern_override_collection


SERVICE_PATTERN_OVERRIDE_REQUIRED_COLUMNS = [
    OVERRIDE_SERVICE_ID_COL_HEADER,
    OVERRIDE_DATE_COL_HEADER,
    OVERRIDE_TYPE_COL_HEADER
]

def parse_service_pattern_overrides(
        file_name: str,
        service_patterns: list[ServicePattern]
) -> list[ServicePatternOverride]:
    """
    Creates a list of ServicePatternOverride objects from the rows in the given
    file, or throws an exception if the file or its content are invalid. If
    created successfully, the ServicePatternOverrides are added to the
    corresponding ServicePattern objects in the given list, or an exception is
    thrown if any foreign key is invalid.
    """
    override_assignments: list[tuple[str, ServicePatternOverride]] = parse_gtfs_file(
        file_name=file_name,
        required_column_names=SERVICE_PATTERN_OVERRIDE_REQUIRED_COLUMNS,
        object_builder_from_row=_create_service_pattern_override_from_row,
        collection_validator=validate_service_pattern_override_collection
    )

    for assignment in override_assignments:
        service_id, override = assignment

        service_pattern = get_service_pattern_from_foreign_key(
            service_id,
            service_patterns
        )

        service_pattern.add_override(override)

    return [override for service_id, override in override_assignments]

def _create_service_pattern_override_from_row(row: dict[str, str | None],
                                              row_num: int) -> tuple[str, ServicePatternOverride]:
    service_id = validate_and_parse_override_service_id(
        row[OVERRIDE_SERVICE_ID_COL_HEADER],
        row_num
    )

    override_date = validate_and_parse_override_date(
        row[OVERRIDE_DATE_COL_HEADER],
        row_num
    )

    override_type = validate_and_parse_override_type(
        row[OVERRIDE_TYPE_COL_HEADER],
        row_num
    )

    return service_id, ServicePatternOverride(override_date, override_type)