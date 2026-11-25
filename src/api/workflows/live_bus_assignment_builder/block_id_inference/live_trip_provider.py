from typing import Protocol
from api.domain.raw_api_data.live_trip import LiveTrip


class LiveTripProvider(Protocol):
    def get_live_trip(self, trip_key: str) -> LiveTrip:
        """
        Returns the LiveTrip corresponding to the given trip key.
        """
        pass