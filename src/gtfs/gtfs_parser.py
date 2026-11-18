from dataclasses import dataclass
from pathlib import Path
from global_packages.database_connection import connection
from gtfs.constants.gtfs_constants import ROUTES_FILE_NAME, STOPS_FILE_NAME, AGENCY_FILE_NAME, FEED_INFO_FILE_NAME, \
    SERVICE_PATTERNS_FILE_NAME, SERVICE_PATTERN_OVERRIDES_FILE_NAME, SHAPES_FILE_NAME, TRIPS_FILE_NAME, \
    STOP_VISITS_FILE_NAME
from gtfs.database_client.postgresql.gtfs_postgresql_eraser import GTFSPostgreSQLEraser
from gtfs.database_client.postgresql.gtfs_postgresql_writer import GTFSPostgreSQLWriter
from gtfs.domain.agency import Agency
from gtfs.domain.feed_info import FeedInfo
from gtfs.domain.route import Route
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.shape.shape import Shape
from gtfs.domain.stop import Stop
from gtfs.domain.trip.trip import Trip
from gtfs.parsing.csv_parsing.agency_parser import parse_agencies
from gtfs.parsing.csv_parsing.feed_info_parser import parse_feed_info
from gtfs.parsing.csv_parsing.route_parser import parse_routes
from gtfs.parsing.csv_parsing.service_pattern_override_parser import parse_service_pattern_overrides
from gtfs.parsing.csv_parsing.service_pattern_parser import parse_service_patterns
from gtfs.parsing.csv_parsing.shape_parser import parse_shapes
from gtfs.parsing.csv_parsing.stop_parser import parse_stops
from gtfs.parsing.csv_parsing.stop_visit_parser import parse_stop_visits
from gtfs.parsing.csv_parsing.trip_parser import parse_trips


def parse_gtfs(csv_input_folder: Path) -> None:
    """
    Parses the GTFS feed from the CSV files in the given directory then writes
    it to the database.
    Assumes that the entire GTFS feed is present in the given directory.
    Does not catch any exceptions.
    """
    parsed_gtfs = _parse_csv_files(csv_input_folder)
    _write_to_database(parsed_gtfs)

@dataclass
class GTFSFeed:
    """
    Stores all elements parsed from the GTFS archive.
    """
    agency: Agency
    feed_info: FeedInfo
    routes: list[Route]
    stops: list[Stop]
    service_patterns: list[ServicePattern]
    shapes: list[Shape]
    trips: list[Trip]

def _parse_csv_files(csv_input_folder: Path) -> GTFSFeed:
    """
    Parses each relevant CSV file in the given folder and creates GTFS domain
    objects. Returns a GTFSFeed containing the agency and feed info, routes,
    stops, service patterns, shapes, and trips.
    Assumes that the entire GTFS feed is present in the given directory.
    Does not catch any exceptions.
    """
    agency = parse_agencies(f"{csv_input_folder}/{AGENCY_FILE_NAME}")[0]
    feed_info = parse_feed_info(f"{csv_input_folder}/{FEED_INFO_FILE_NAME}")

    routes = parse_routes(f"{csv_input_folder}/{ROUTES_FILE_NAME}")
    stops = parse_stops(f"{csv_input_folder}/{STOPS_FILE_NAME}")

    service_patterns = parse_service_patterns(
        f"{csv_input_folder}/{SERVICE_PATTERNS_FILE_NAME}"
    )
    parse_service_pattern_overrides(
        f"{csv_input_folder}/{SERVICE_PATTERN_OVERRIDES_FILE_NAME}",
        service_patterns=service_patterns
    )

    shapes = parse_shapes(f"{csv_input_folder}/{SHAPES_FILE_NAME}")

    trips = parse_trips(
        f"{csv_input_folder}/{TRIPS_FILE_NAME}",
        routes=routes,
        service_patterns=service_patterns,
        shapes=shapes
    )
    parse_stop_visits(
        f"{csv_input_folder}/{STOP_VISITS_FILE_NAME}",
        trips=trips,
        stops=stops
    )

    return GTFSFeed(
        agency=agency,
        feed_info=feed_info,
        routes=list(routes.values()),
        stops=list(stops.values()),
        service_patterns=list(service_patterns.values()),
        shapes=list(shapes.values()),
        trips=list(trips.values())
    )

def _write_to_database(parsed_gtfs: GTFSFeed) -> None:
    """
    Writes the given GTFSFeed to the database in one transaction.
    Does not catch any exceptions. Clears any previously stored data.
    """
    with connection() as db:
        eraser = GTFSPostgreSQLEraser(db)
        writer = GTFSPostgreSQLWriter(db)

        eraser.clear_tables()

        writer.write_agency(parsed_gtfs.agency)
        writer.write_feed_info(parsed_gtfs.feed_info)

        for route in parsed_gtfs.routes:
            writer.write_route(route)

        for stop in parsed_gtfs.stops:
            writer.write_stop(stop)

        for service_pattern in parsed_gtfs.service_patterns:
            writer.write_service_pattern_and_overrides(service_pattern)

        for shape in parsed_gtfs.shapes:
            writer.write_shape_and_points(shape)

        for trip in parsed_gtfs.trips:
            writer.write_trip_and_stop_visits(trip)
