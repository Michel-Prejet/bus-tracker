import validators
from global_packages.utilities.invariant_helper import require_type, require_state


class Url:
    """
    Enforces validity on a URL read from the GTFS.
    """

    def __init__(self, url: str) -> None:
        self._url = url

        self._check_url()

    @property
    def value(self) -> str:
        return self._url

    def _check_url(self) -> None:
        require_type(str, url_string=self._url)

        require_state(
            validators.url(self._url),
            "URL string should correspond to a valid URL."
        )
