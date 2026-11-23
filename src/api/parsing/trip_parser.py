from typing import Any
from api.domain.raw_api_data.live_stop_visit import LiveStopVisit
from api.domain.raw_api_data.live_trip import LiveTrip
from api.parsing.helpers.json_parsing_factory import JsonParsingFactory
from api.parsing.times_parser import parse_times
from global_packages.value_parsing.datetime_parser import parse_time


def parse_api_trip(
    response: dict[str, Any],
    api_resource_url: str
) -> LiveTrip:
    """
    Creates a LiveTrip object from the trip described in the given Winnipeg
    Transit API response. Tokens are validated and exceptions are thrown if any
    required data is missing, or if any token is invalid.
    """
    stop_visits: list[LiveStopVisit] = []

    parser = JsonParsingFactory(
        api_resource_url=api_resource_url,
        root=response
    )
    parser = parser.next("trip")

    trip_key = parser.get("key", expected_type=int)

    for scheduled_stop_parser in parser.next_as_list("scheduled-stops"):
        stop_id = scheduled_stop_parser.next("stop").get("key", expected_type=int)

        times = parse_times(
            scheduled_stop_parser.next("times"),
            time_parsing_function=parse_time
        )

        stop_visits.append(LiveStopVisit(
            stop_id=str(stop_id),
            times=times
        ))

    return LiveTrip(
        trip_key=str(trip_key),
        stop_visits=stop_visits
    )