from gtfs.constants.csv_column_headers.service_pattern_override_headers import OVERRIDE_SERVICE_ID_COL_HEADER, \
    OVERRIDE_DATE_COL_HEADER, OVERRIDE_TYPE_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import parse_gtfs_file
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.service_pattern.service_pattern_override import ServicePatternOverride
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.service_pattern_override_validator import validate_and_parse_override_type, \
    validate_service_pattern_override_collection, validate_and_parse_override_service_id_as_foreign_key, \
    validate_and_parse_override_date
from invariant_helper import require_not_none


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
    override_assignments: list[tuple[ServicePattern, ServicePatternOverride]] = parse_gtfs_file(
        file_name=file_name,
        required_column_names=SERVICE_PATTERN_OVERRIDE_REQUIRED_COLUMNS,
        object_builder_from_row=(
            lambda row, row_num:
            _create_service_pattern_override_from_row(row, row_num, service_patterns)
        ),
        collection_validator=validate_service_pattern_override_collection
    )

    for pattern, override in override_assignments:
        pattern.add_override(override)

    return [override for pattern, override in override_assignments]

def _create_service_pattern_override_from_row(
        row: dict[str, str],
        row_num: int,
        service_patterns: list[ServicePattern]
) -> tuple[ServicePattern, ServicePatternOverride]:
    require_not_none(row=row, service_pattern_list=service_patterns)
    for pattern in service_patterns:
        require_not_none(service_pattern_in_list=pattern)
    require_valid_row_num(row_num)

    service_id = validate_and_parse_override_service_id_as_foreign_key(
        row[OVERRIDE_SERVICE_ID_COL_HEADER],
        service_patterns,
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