from gtfs.exceptions.domain_error import DomainError


def assert_at_least_one_not_none(value1: str | None, value2: str | None) -> None:
    """
    Throws an exception if both of the given strings are None.
    """
    if value1 is None and value2 is None:
        raise DomainError

def assert_not_greater_than[T](value1: T, value2: T) -> None:
    """
    Throws an exception if the first object is greater than the second.
    """
    if value1 > value2:
        raise DomainError