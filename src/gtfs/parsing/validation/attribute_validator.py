from gtfs.exceptions.domain_error import DomainError


def assert_nonnegative(value: int) -> None:
    """
    Throws an exception if the given integer is negative.
    """
    if value < 0 :
        raise DomainError

