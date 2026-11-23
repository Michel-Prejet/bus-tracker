from datetime import date
from api.domain.inferred_api_data.bus import Bus
from api.domain.inferred_api_data.bus_assignment import BusAssignment
from api.domain.raw_api_data.bus_observation import BusObservation
from global_packages.utilities.invariant_helper import require_type, require_state
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID


class LiveBusAssignment:
    """
    Represents an assignment of a bus to a block, inferred from a list of bus
    observations.
    """

    def __init__(
        self,
        assignment: BusAssignment,
        cancelled: bool | None,
        bike_rack: bool | None,
        observations: list[BusObservation]
    ):
        self._assignment = assignment
        self._cancelled = cancelled
        self._bike_rack = bike_rack
        self._observations = observations

        self._check_bus_assignment()

        self._observations = self._observations.copy()

    @property
    def bus(self) -> Bus:
        return self._assignment.bus

    @property
    def block_id(self) -> WinnipegBlockID:
        return self._assignment.block_id

    @property
    def service_date(self) -> date:
        return self._assignment.service_date

    @property
    def cancelled(self) -> bool | None:
        return self._cancelled

    @property
    def bike_rack(self) -> bool | None:
        return self._bike_rack

    @property
    def observations(self) -> list[BusObservation]:
        return self._observations.copy()

    def _check_bus_assignment(self) -> None:
        require_type(BusAssignment, bus_assignment=self._assignment)
        require_type(
            bool | None,
            cancelled_status=self._cancelled,
            bike_rack_status=self._bike_rack
        )
        require_type(list, bus_observation_list=self._observations)

        require_state(
            len(self._observations) > 0,
            "List of bus observations should not be empty."
        )

        for obs in self._observations:
            require_type(BusObservation, bus_observation_in_list=obs)

            require_state(
                self._assignment.bus.tracking_number == obs.bus_tracking_num,
                "Bus observation in list should have the same tracking number "
                "as the associated bus assignment."
            )

            require_state(
                self._assignment.service_date == obs.service_date,
                "Bus observation in list should have the same service "
                "date as the associated bus assignment."
            )

        require_state(
            all(
                o.bike_rack is None or o.bike_rack == self._bike_rack
                for o in self._observations
            ),
            "Every known bike rack status must agree with the assignment."
        )
        require_state(
            self._bike_rack is None
            or any(o.bike_rack == self._bike_rack for o in self._observations),
            "A known bike rack status must be supported by an observation."
        )

        if self._cancelled is None:
            require_state(
                all(o.cancelled is None for o in self._observations),
                "A unknown cancelled status is only possible when the "
                "cancelled status of all bus observations is also unknow."
            )
        elif self._cancelled:
            require_state(
                any(o.cancelled for o in self._observations),
                "A cancelled live bus assignment should contain at "
                "least one cancelled bus observation."
            )
        else:
            require_state(
                (
                    all(not o.cancelled for o in self._observations) and
                    any(o.cancelled is False for o in self._observations)
                ),
                "A live bus assignment that is not cancelled should "
                "contain at least one bus observation that is not cancelled, "
                "and no bus observations that are cancelled."
            )
