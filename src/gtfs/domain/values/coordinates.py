from gtfs.gtfs_constants import MIN_LATITUDE, MAX_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE
from utilities.invariant_helper import require_not_none, require_state


class Coordinates:
    """
    Enforces validity on a set of coordinates, represented as floats.
    """

    def __init__(self, latitude: float, longitude: float):
        self._latitude = latitude
        self._longitude = longitude

        self._check_coordinates()

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    def _check_coordinates(self) -> None:
        require_not_none(
            latitude=self._latitude,
            longitude=self._longitude
        )

        require_state(
            MIN_LATITUDE <= self._latitude <= MAX_LATITUDE,
            f"Latitude should be in the interval [{MIN_LATITUDE}, {MAX_LATITUDE}]."
        )
        require_state(
            MIN_LONGITUDE <= self._longitude <= MAX_LONGITUDE,
            f"Longitude should be in the interval [{MIN_LONGITUDE}, {MAX_LONGITUDE}]."
        )