from datetime import timedelta
from global_packages.exceptions.domain_error import DomainError


def assert_nonnegative_time(value: timedelta) -> None:
    """
    Throws a DomainError if the given timedelta is negative.
    """
    if value < timedelta(0):
        raise DomainError

def validate_times(
        scheduled_departure: timedelta | None,
        scheduled_arrival: timedelta | None,
        estimated_departure: timedelta | None,
        estimated_arrival: timedelta | None
) -> None:
    """
    Throws a DomainError if both scheduled times are None, or if any arrival
    times are greater than their corresponding departure times.
    """
    if scheduled_departure is None and scheduled_arrival is None:
        raise DomainError

    if scheduled_departure is not None and scheduled_arrival is not None:
        if scheduled_arrival > scheduled_departure:
            raise DomainError

    if estimated_departure is not None and estimated_arrival is not None:
        if estimated_arrival > estimated_departure:
            raise DomainError


