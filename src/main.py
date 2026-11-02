from gtfs.constants.gtfs_constants import ROUTES_FILE_NAME, STOPS_FILE_NAME, SERVICE_PATTERNS_FILE_NAME, \
    SERVICE_PATTERN_OVERRIDES_FILE_NAME
from gtfs.csv_parsing.route_parser import parse_routes
from gtfs.csv_parsing.service_pattern_override_parser import parse_service_pattern_overrides
from gtfs.csv_parsing.service_pattern_parser import parse_service_patterns
from gtfs.csv_parsing.stop_parser import parse_stops
from gtfs.error_messages import get_err_msg

try:
    routes = parse_routes(ROUTES_FILE_NAME)

    stops = parse_stops(STOPS_FILE_NAME)

    service_patterns = parse_service_patterns(SERVICE_PATTERNS_FILE_NAME)

    service_pattern_overrides = parse_service_pattern_overrides(
        SERVICE_PATTERN_OVERRIDES_FILE_NAME,
        service_patterns
    )
except Exception as e:
    print(get_err_msg(e))