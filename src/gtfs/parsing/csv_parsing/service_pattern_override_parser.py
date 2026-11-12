from gtfs.constants.csv_column_headers.service_pattern_override_headers import OVERRIDE_SERVICE_ID_COL_HEADER, \
    OVERRIDE_DATE_COL_HEADER, OVERRIDE_TYPE_COL_HEADER
from gtfs.constants.gtfs_constants import SERVICE_PATTERN_OVERRIDES_FILE_NAME, SERVICE_PATTERNS_FILE_NAME
from gtfs.parsing.helpers.gtfs_file_parser import parse_gtfs_file
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.service_pattern.service_pattern_override import ServicePatternOverride
from gtfs.parsing.helpers.row_parsing_factory import RowParsingFactory
from gtfs.parsing.validation.collection_validator import validate_service_pattern_overrides
from gtfs.parsing.value_parsing.datetime_parser import parse_date
from gtfs.parsing.value_parsing.enum_parser import parse_override_type
from gtfs.parsing.value_parsing.primitive_parser import parse_string


SERVICE_PATTERN_OVERRIDE_REQUIRED_COLUMNS = [
    OVERRIDE_SERVICE_ID_COL_HEADER,
    OVERRIDE_DATE_COL_HEADER,
    OVERRIDE_TYPE_COL_HEADER
]

def parse_service_pattern_overrides(
        file_name: str,
        service_patterns: dict[str, ServicePattern]
) -> list[ServicePatternOverride]:
    """
    Creates a list of ServicePatternOverride objects from the rows in the given
    file, or throws an exception if the file or its content are invalid. If
    created successfully, the ServicePatternOverrides are added to the
    corresponding ServicePattern objects in the given dictionary, or an
    exception is thrown if any foreign key is invalid.
    """
    override_assignments: list[tuple[ServicePattern, ServicePatternOverride]] = parse_gtfs_file(
        file_name=file_name,
        required_column_names=SERVICE_PATTERN_OVERRIDE_REQUIRED_COLUMNS,
        object_builder_from_row=(
            lambda row, row_num:
            _create_service_pattern_override_from_row(row, row_num, service_patterns)
        ),
        collection_validator=validate_service_pattern_overrides
    )

    for pattern, override in override_assignments:
        pattern.add_override(override)

    return [override for pattern, override in override_assignments]

def _create_service_pattern_override_from_row(
        row: dict[str, str | None],
        row_num: int,
        service_patterns: dict[str, ServicePattern]
) -> tuple[ServicePattern, ServicePatternOverride]:
    parser = RowParsingFactory(
        file_name=SERVICE_PATTERN_OVERRIDES_FILE_NAME,
        row=row,
        row_num=row_num
    )

    service_pattern = parser.get_attribute_as_foreign_key(
        column_name=OVERRIDE_SERVICE_ID_COL_HEADER,
        referenced_objs=service_patterns,
        referenced_file_name=SERVICE_PATTERNS_FILE_NAME,
        parser=parse_string
    )

    override_date = parser.get_attribute(
        column_name=OVERRIDE_DATE_COL_HEADER,
        parser=parse_date
    )

    override_type = parser.get_attribute(
        column_name=OVERRIDE_TYPE_COL_HEADER,
        parser=parse_override_type
    )

    return service_pattern, ServicePatternOverride(override_date, override_type)