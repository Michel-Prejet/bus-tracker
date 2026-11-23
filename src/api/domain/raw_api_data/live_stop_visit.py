from datetime import timedelta
from api.domain.raw_api_data.times import Times
from global_packages.utilities.invariant_helper import require_type, require_non_empty_str


class LiveStopVisit:
    """
    Represents a live stop visit recorded from the Winnipeg Transit API.
    """

    def __init__(self, stop_id: str, times: Times):
        self._stop_id = stop_id
        self._times = times

        self._check_live_stop_visit()

    @property
    def stop_id(self) -> str:
        return self._stop_id

    @property
    def scheduled_departure(self) -> timedelta | None:
        return self._times.scheduled_departure

    @property
    def scheduled_arrival(self) -> timedelta | None:
        return self._times.scheduled_arrival

    @property
    def estimated_departure(self) -> timedelta | None:
        return self._times.estimated_departure

    @property
    def estimated_arrival(self) -> timedelta | None:
        return self._times.estimated_arrival

    def _check_live_stop_visit(self) -> None:
        require_type(str, stop_id=self._stop_id)
        require_type(Times, stop_times=self._times)

        require_non_empty_str(stop_id=self._stop_id)