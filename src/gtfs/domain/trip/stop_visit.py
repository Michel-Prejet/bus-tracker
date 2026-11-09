from datetime import timedelta
from gtfs.domain.stop import Stop
from invariant_helper import require_state, require_type


class StopVisit:
    """
    Represents a scheduled visit at a stop in a particular trip. Stores
    the stop, its sequence order in the trip, and scheduled arrival/departure
    times.
    """

    def __init__(
            self,
            stop: Stop,
            scheduled_arrival: timedelta,
            scheduled_departure: timedelta,
            sequence_order: int
    ):
        self._stop = stop
        self._scheduled_arrival = scheduled_arrival
        self._scheduled_departure = scheduled_departure
        self._sequence_order = sequence_order

        self._check_stop_visit()

    def __lt__(self, other: "StopVisit") -> bool:
        """
        Returns True if this stop visit's sequence order is less than the
        given stop visit's sequence order; returns False otherwise.
        """
        if not isinstance(other, StopVisit):
            return NotImplemented

        return self._sequence_order < other.sequence_order

    @property
    def stop(self) -> Stop:
        return self._stop

    @property
    def scheduled_arrival(self) -> timedelta:
        return self._scheduled_arrival

    @property
    def scheduled_departure(self) -> timedelta:
        return self._scheduled_departure

    @property
    def sequence_order(self) -> int:
        return self._sequence_order

    def _check_stop_visit(self) -> None:
        require_type(Stop, stop_visit_stop=self._stop)
        require_type(int, stop_visit_sequence_order=self._sequence_order)
        require_type(timedelta,
                     stop_visit_scheduled_arrival=self._scheduled_arrival)
        require_type(timedelta,
                     stop_visit_scheduled_departure=self._scheduled_departure)

        require_state(
            self._scheduled_arrival >= timedelta(0),
            "Scheduled stop arrival should not be negative."
        )
        require_state(
            self._scheduled_departure >= timedelta(0),
            "Scheduled stop departure should not be negative."
        )
        require_state(
            self._scheduled_arrival <= self._scheduled_departure,
            "Scheduled stop arrival should not be after the scheduled departure."
        )

        require_state(
            self._sequence_order >= 0,
            "Stop visit sequence order should not be negative."
        )