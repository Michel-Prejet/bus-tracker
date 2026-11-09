from gtfs.domain.route import Route
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.shape.shape import Shape
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID
from gtfs.constants.gtfs_constants import TRIP_DIRECTION_VALUES
from invariant_helper import require_not_none, require_state, require_non_empty_str, require_type
from gtfs.domain.trip.stop_visit import StopVisit
from bisect import insort


class Trip:
    """
    Represents a trip consisting of a sequence of stops on a route following a
    shape. The trip may be part of a block, which is defined for a specific
    service pattern (e.g. block 1-1 on weekday service). Also stores the
    headsign displayed on the trip, and its direction.
    """

    def __init__(
            self,
            trip_id: str,
            route: Route,
            service_pattern: ServicePattern,
            block: WinnipegBlockID,
            shape: Shape | None,
            headsign: str | None,
            direction: int | None
    ):
        self._trip_id = trip_id
        self._route = route
        self._stop_visits: list[StopVisit] = []
        self._service_pattern = service_pattern
        self._block = block
        self._shape = shape
        self._headsign = headsign
        self._direction = direction

        self._check_trip()

    @property
    def id(self) -> str:
        return self._trip_id

    @property
    def route(self) -> Route:
        return self._route

    @property
    def stop_visits(self) -> list[StopVisit]:
        """
        Returns a shallow copy of the list of stop visits for this trip,
        sorted in increasing sequential order.
        """
        return self._stop_visits.copy()

    @property
    def service_pattern(self) -> ServicePattern:
        return self._service_pattern

    @property
    def block(self) -> WinnipegBlockID:
        return self._block

    @property
    def shape(self) -> Shape | None:
        return self._shape

    @property
    def headsign(self) -> str | None:
        return self._headsign

    @property
    def direction(self) -> int | None:
        return self._direction

    def add_stop_visit(self, stop_visit: StopVisit) -> None:
        """
        Adds the given stop visit to this trip, maintaining the ordered list
        so that it is sorted by strictly increasing sequential orders of the
        stop visits.
        Assumes that there is no stop visit in the list with the same
        sequential order.
        """
        insort(self._stop_visits, stop_visit)

        self._check_trip()

    def _check_trip(self) -> None:
        require_type(str, trip_id=self._trip_id)
        require_type(Route, trip_route=self._route)
        require_type(ServicePattern, trip_service_pattern=self._service_pattern)
        require_type(WinnipegBlockID, trip_block_id=self._block)
        require_type(Shape, trip_shape=self._shape)
        require_type(str | None, trip_headsign=self._headsign)
        require_type(int | None, trip_direction=self._direction)

        require_non_empty_str(trip_id=self._trip_id)

        prev_seq_order: int | None = None
        for visit in self._stop_visits:
            if prev_seq_order is not None:
                require_state(
                    prev_seq_order < visit.sequence_order,
                    "Stop visits should be sorted by strictly "
                    "increasing sequence order."
                )

                prev_seq_order = visit.sequence_order

        if self._block is not None:
            require_state(
                self._block.service_id == self._service_pattern.service_id,
                "The trip's service ID should match the service ID of its block."
            )

        if self._headsign is not None:
            require_non_empty_str(trip_headsign=self._headsign)

        if self._direction is not None:
            require_state(
                self._direction in TRIP_DIRECTION_VALUES,
                f"The trip direction should be a value in [{TRIP_DIRECTION_VALUES}]."
            )