from gtfs.domain.values.coordinates import Coordinates
from gtfs.domain.values.url import Url
from utilities.invariant_helper import require_not_none, require_non_empty_str


class Stop:
    """
    Represents a stop read from the GTFS with an ID, a stop code, a name,
    coordinates, and a URL.

    The official GTFS invariants for this object are as follows:
    * The ID cannot be None or empty.
    * If the stop code is not None, it cannot be empty.
    * The stop name cannot be None or empty.
    * The coordinates cannot be None.
    """

    def __init__(
            self,
            stop_id: str,
            stop_code: str | None,
            name: str,
            coordinates: Coordinates,
            stop_url: Url | None
    ):
        self._stop_id = stop_id
        self._stop_code = stop_code
        self._name = name
        self._coordinates = coordinates
        self._stop_url = stop_url

        self._check_stop()

    @property
    def id(self) -> str:
        """
        Returns the internal ID used to reference this stop within the GTFS.
        """
        return self._stop_id

    @property
    def code(self) -> str | None:
        """
        Returns the passenger-facing stop code, or None if no such attribute
        has been defined.
        """
        return self._stop_code

    @property
    def name(self) -> str:
        return self._name

    @property
    def coordinates(self) -> Coordinates:
        return self._coordinates

    @property
    def url(self) -> Url | None:
        return self._stop_url

    def _check_stop(self) -> None:
        require_not_none(
            stop_id=self._stop_id,
            stop_name=self._name,
            stop_coordinates=self._coordinates
        )

        require_non_empty_str(stop_id=self._stop_id)

        if self._stop_code is not None:
            require_non_empty_str(stop_code=self._stop_code)

        require_non_empty_str(stop_name=self._name)