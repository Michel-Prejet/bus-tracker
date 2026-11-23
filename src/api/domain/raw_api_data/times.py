from datetime import timedelta
from global_packages.utilities.invariant_helper import require_type, require_state


class Times:
    """
    Stores arrival and departure times for a stop visit, both scheduled and
    estimated.
    All times are optional on their own, but one of the scheduled times must be
    included.
    """

    def __init__(
        self,
        scheduled_departure: timedelta | None,
        scheduled_arrival: timedelta | None,
        estimated_departure: timedelta | None,
        estimated_arrival: timedelta | None,
    ):
        self._scheduled_departure = scheduled_departure
        self._scheduled_arrival = scheduled_arrival
        self._estimated_departure = estimated_departure
        self._estimated_arrival = estimated_arrival

        self._check_times()

    @property
    def scheduled_departure(self) -> timedelta:
        return self._scheduled_departure

    @property
    def scheduled_arrival(self) -> timedelta | None:
        return self._scheduled_arrival

    @property
    def estimated_departure(self) -> timedelta | None:
        return self._estimated_departure

    @property
    def estimated_arrival(self) -> timedelta | None:
        return self._estimated_arrival

    def _check_times(self) -> None:
        require_type(
            timedelta | None,
            scheduled_departure=self._scheduled_departure,
            scheduled_arrival=self._scheduled_arrival,
            estimated_departure=self._estimated_departure,
            estimated_arrival=self._estimated_arrival
        )

        require_state(
            self._scheduled_departure is not None or
            self._scheduled_arrival is not None,
            "The scheduled arrival and departure times cannot both be None."
        )

        if self._scheduled_departure is not None:
            require_state(
                self._scheduled_departure >= timedelta(0),
                "Scheduled departure time should not be negative."
            )

        if self._scheduled_arrival is not None:
            require_state(
                self._scheduled_arrival >= timedelta(0),
                "Scheduled arrival time should not be negative."
            )

        if self._estimated_departure is not None:
            require_state(
                self._estimated_departure >= timedelta(0),
                "Estimated departure time should not be negative."
            )

        if self._estimated_arrival is not None:
            require_state(
                self._estimated_arrival >= timedelta(0),
                "Estimated arrival time should not be negative."
            )

        if (self._scheduled_arrival is not None and
            self._scheduled_departure is not None):
            require_state(
                self._scheduled_arrival <= self._scheduled_departure,
                "Scheduled departure time should not come after the scheduled arrival time."
            )

        if (self._estimated_arrival is not None and
            self._estimated_departure is not None):
            require_state(
                self._estimated_arrival <= self._estimated_departure,
                "Estimated departure time should not come after the estimated arrival time."
            )
