from api.domain.raw_api_data.live_stop_visit import LiveStopVisit
from global_packages.utilities.invariant_helper import require_type, require_non_empty_str, require_state


class LiveTrip:
    """
    A live trip reconstructed from the Winnipeg Transit API, with a list of
    scheduled stop visits.
    Expects stop visits to be in the order that they will be made by the bus.
    """

    def __init__(self, trip_key: str, stop_visits: list[LiveStopVisit]):
        self._trip_key = trip_key
        self._stop_visits = stop_visits

        self._check_live_trip()

        self._stop_visits = self._stop_visits.copy()

    @property
    def trip_key(self) -> str:
        return self._trip_key

    @property
    def stop_visits(self) -> list[LiveStopVisit]:
        """
        Returns a shallow copy of the list of stop visits.
        """
        return self._stop_visits.copy()

    def _check_live_trip(self) -> None:
        require_type(str, trip_key=self._trip_key)
        require_type(list, live_stop_visit_list=self._stop_visits)
        for visit in self._stop_visits:
            require_type(LiveStopVisit, live_stop_visit_in_list=visit)

        require_non_empty_str(trip_key=self._trip_key)
