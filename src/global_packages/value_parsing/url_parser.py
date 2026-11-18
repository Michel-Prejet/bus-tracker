import validators
from global_packages.exceptions.value_parsing_error import ValueParsingError
from gtfs.domain.values.url import Url


def parse_url(raw: str) -> Url:
    """
    Throws an exception if the given string is not a valid URL; otherwise
    returns a URL object.
    """
    raw = raw.strip()

    if not validators.url(raw):
        raise ValueParsingError

    return Url(raw)