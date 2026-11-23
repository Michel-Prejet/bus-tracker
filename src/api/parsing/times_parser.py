from datetime import timedelta
from typing import Callable
from api.domain.raw_api_data.times import Times
from api.parsing.helpers.json_parsing_factory import JsonParsingFactory
from api.parsing.validation.times_validator import assert_nonnegative_time, validate_times


def parse_times(
        parser: JsonParsingFactory,
        time_parsing_function: Callable[[str], timedelta]
) -> Times:
    """
    Creates a Times object containing scheduled and estimated arrival and
    departure times read from the given parser.
    Expects the root of the given parser to contain "departure" and "arrival"
    keys, each of which contain "scheduled" and "estimated" keys.
    An exception is thrown if the times are invalid or if both scheduled times
    are missing.
    """
    departure_parser = parser.next("departure", optional=True)
    arrival_parser = parser.next("arrival", optional=True)

    if departure_parser is not None:
        scheduled_departure = departure_parser.get(
            "scheduled",
            expected_type=str,
            parser=time_parsing_function,
            validator=assert_nonnegative_time,
            optional=True
        )

        estimated_departure = departure_parser.get(
            "estimated",
            expected_type=str,
            parser=time_parsing_function,
            validator=assert_nonnegative_time,
            optional=True
        )
    else:
        scheduled_departure = None
        estimated_departure = None

    if arrival_parser is not None:
        scheduled_arrival = arrival_parser.get(
            "scheduled",
            expected_type=str,
            parser=time_parsing_function,
            validator=assert_nonnegative_time,
            optional=True
        )

        estimated_arrival = arrival_parser.get(
            "estimated",
            expected_type=str,
            parser=time_parsing_function,
            validator=assert_nonnegative_time,
            optional=True
        )
    else:
        scheduled_arrival = None
        estimated_arrival = None

    parser.assert_valid_attribute_combination(
        lambda: validate_times(
            scheduled_departure=scheduled_departure,
            scheduled_arrival=scheduled_arrival,
            estimated_departure=estimated_departure,
            estimated_arrival=estimated_arrival
        ),
        [
            str(scheduled_departure),
            str(scheduled_arrival),
            str(estimated_departure),
            str(estimated_arrival)
        ]
    )

    return Times(
        scheduled_departure=scheduled_departure,
        estimated_departure=estimated_departure,
        scheduled_arrival=scheduled_arrival,
        estimated_arrival=estimated_arrival,
    )