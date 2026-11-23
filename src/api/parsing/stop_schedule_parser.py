from datetime import date, timedelta
from typing import Any, Callable
from zoneinfo import ZoneInfo
from api.domain.raw_api_data.bus_observation import BusObservation
from api.domain.raw_api_data.live_stop_visit import LiveStopVisit
from api.parsing.helpers.json_parsing_factory import JsonParsingFactory
from api.parsing.times_parser import parse_times
from api.parsing.validation.times_validator import assert_nonnegative_time
from global_packages.value_parsing.datetime_parser import parse_time_as_offset
from global_packages.value_parsing.primitive_parser import parse_bool


def parse_api_stop_schedule(
    response: dict[str, Any],
    api_resource_url: str,
    service_date: date,
    timezone: ZoneInfo
) -> list[BusObservation]:
    """
    Creates a BusObservation object for each scheduled stop in the given
    Winnipeg Transit API stop schedule, then returns the results in a list.
    Tokens are validated and exceptions are thrown if any required data is
    missing, or if any token is invalid.
    Any observation in which bus information is missing is silently ignored.
    """
    observations: list[BusObservation] = []

    parser = JsonParsingFactory(
        api_resource_url=api_resource_url,
        root=response
    )

    time_parsing_function = lambda raw: (
        parse_time_as_offset(raw, service_date, timezone)
    )

    query_time = parser.get(
        "query-time",
        expected_type=str,
        parser=time_parsing_function,
        validator=assert_nonnegative_time
    )

    parser = parser.next("stop-schedule")

    stop_id = parser.next("stop").get("key", expected_type=int)

    for route_schedule_parser in parser.next_as_list("route-schedules"):
        route_id = (
            route_schedule_parser.next("route").
            get("key", expected_type=str | int)
        )

        for scheduled_stop_parser in route_schedule_parser.next_as_list("scheduled-stops"):
            observation = _parse_scheduled_stop(
                parser=scheduled_stop_parser,
                query_time=query_time,
                stop_id=stop_id,
                route_id=route_id,
                service_date=service_date,
                time_parsing_function=time_parsing_function
            )

            if observation is not None:
                observations.append(
                    _parse_scheduled_stop(
                        parser=scheduled_stop_parser,
                        query_time=query_time,
                        stop_id=stop_id,
                        route_id=route_id,
                        service_date=service_date,
                        time_parsing_function=time_parsing_function
                    )
                )

    return observations

def _parse_scheduled_stop(
    parser: JsonParsingFactory,
    query_time: timedelta,
    stop_id: int,
    route_id: str | int,
    service_date: date,
    time_parsing_function: Callable[[str], timedelta]
) -> BusObservation | None:
    trip_key = parser.get("trip-key", expected_type=int)

    cancelled = parser.get(
        "cancelled",
        expected_type=str,
        parser=parse_bool,
        optional=True
    )

    bus_info_parser = parser.next("bus", optional=True)
    if bus_info_parser is None:
        return None

    bus_tracking_num = bus_info_parser.get("key", expected_type=int)

    bike_rack = parser.next("bus").get(
        "bike-rack",
        expected_type=str,
        parser=parse_bool,
        optional=True
    )

    times = parse_times(
        parser.next("times"),
        time_parsing_function=time_parsing_function
    )

    return BusObservation(
        stop_visit=LiveStopVisit(
            stop_id=str(stop_id),
            times=times
        ),
        service_date=service_date,
        bus_tracking_num=str(bus_tracking_num),
        trip_key=str(trip_key),
        route_id=str(route_id),
        cancelled=cancelled,
        bike_rack=bike_rack,
        query_time=query_time
    )