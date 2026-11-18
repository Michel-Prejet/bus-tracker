from datetime import date
from typing import Any, Callable
from zoneinfo import ZoneInfo
from api.api_constants import STOP_SCHEDULE_RESOURCE_NAME
from api.domain.bus_observation import BusObservation
from api.domain.observed_stop_visit import ObservedStopVisit
from api.parsing.json_parsing_factory import JsonParsingFactory
from global_packages.value_parsing.datetime_parser import parse_iso_time_as_gtfs_timestamp
from global_packages.value_parsing.primitive_parser import parse_bool
from gtfs.domain.values.gtfs_timestamp import GTFSTimestamp


def parse_api_stop_schedule(
        schedule: dict[str, Any],
        service_date: date,
        timezone: ZoneInfo
) -> list[BusObservation]:
    """
    Creates a BusObservation object for each scheduled stop in the given
    Winnipeg Transit API stop schedule, then returns the results in a list.
    Tokens are validated and exceptions are thrown if any required data is
    missing, or if any token is invalid.
    """
    observations: list[BusObservation] = []

    parser = JsonParsingFactory(
        api_resource_name=STOP_SCHEDULE_RESOURCE_NAME,
        root=schedule
    )

    time_parsing_function = lambda raw: (
        parse_iso_time_as_gtfs_timestamp(raw, service_date, timezone)
    )

    query_time = parser.get(
        "query-time",
        expected_type=str,
        parser=time_parsing_function
    )

    parser = parser.next("stop-schedule")
    stop_id = parser.next("stop").get("key", expected_type=int)

    for route_schedule_parser in parser.next_as_list("route-schedules"):
        route_id = (
            route_schedule_parser.next("route")
            .get("key", expected_type=str | int)
        )

        for scheduled_stop_parser in (
                route_schedule_parser.next_as_list("scheduled-stops")
        ):
            observation = _get_observation_from_scheduled_stop(
                parser=scheduled_stop_parser,
                time_parsing_function=time_parsing_function,
                query_time=query_time,
                stop_id=stop_id,
                route_id=route_id
            )
            observations.append(observation)

    return observations

def _get_observation_from_scheduled_stop(
        parser: JsonParsingFactory,
        time_parsing_function: Callable,
        query_time: GTFSTimestamp,
        stop_id: int,
        route_id: int | str
) -> BusObservation:
    trip_key = parser.get(
        "trip-key", expected_type=int
    )

    cancelled = parser.get(
        "cancelled",
        expected_type=str,
        parser=parse_bool,
        optional=True
    )

    time_parser = parser.next("times")

    arrival_parser = time_parser.next("arrival", optional=True)
    scheduled_arrival, estimated_arrival = _get_scheduled_and_estimated_times(
        parser=arrival_parser,
        time_parsing_function=time_parsing_function
    )

    departure_parser = time_parser.next("departure", optional=True)
    scheduled_departure, estimated_departure = _get_scheduled_and_estimated_times(
        parser=departure_parser,
        time_parsing_function=time_parsing_function,
        scheduled_is_optional=False
    )

    bus_info_parser = parser.next("bus")
    bus_tracking_num = bus_info_parser.get("key", expected_type=int)
    bike_rack = bus_info_parser.get(
        "bike-rack",
        expected_type=str,
        parser=parse_bool,
        optional=True
    )

    return BusObservation(
        ObservedStopVisit(
            stop_id=str(stop_id),
            scheduled_arrival=scheduled_arrival,
            estimated_arrival=estimated_arrival,
            scheduled_departure=scheduled_departure,
            estimated_departure=estimated_departure
        ),
        bus_tracking_num=str(bus_tracking_num),
        trip_key=str(trip_key),
        route_id=str(route_id),
        query_time=query_time,
        cancelled=cancelled,
        bike_rack=bike_rack
    )


def _get_scheduled_and_estimated_times(
        parser: JsonParsingFactory | None,
        time_parsing_function: Callable,
        scheduled_is_optional: bool = True
) -> tuple[GTFSTimestamp | None, GTFSTimestamp | None]:
    if parser is None:
        return None, None

    scheduled = parser.get(
        "scheduled",
        expected_type=str,
        parser=time_parsing_function,
        optional=scheduled_is_optional
    )

    estimated = parser.get(
        "estimated",
        expected_type=str,
        parser=time_parsing_function,
        optional=True
    )

    return scheduled, estimated