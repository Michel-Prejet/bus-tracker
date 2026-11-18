from datetime import date
from api.domain.bus import Bus
from api.domain.bus_observation import BusObservation
from api.domain.enums.block_assignment_status import BlockAssignmentStatus
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID
from global_packages.utilities.invariant_helper import require_type, require_state


class BlockAssignment:
    """
    Represents an assignment of a bus to a block, along with the status of the
    assignment (scheduled, active, or cancelled) and the list of observations
    from which the assignment was inferred.
    """

    def __init__(
        self,
        bus: Bus,
        block_id: WinnipegBlockID,
        service_date: date,
        status: BlockAssignmentStatus,
        observations: list[BusObservation]
    ) -> None:
        self._bus = bus
        self._block_id = block_id
        self._service_date = service_date
        self._status = status
        self._observations = observations.copy()

        self._check_block_assignment()

    @property
    def bus(self) -> Bus:
        return self._bus

    @property
    def block_id(self) -> WinnipegBlockID:
        return self._block_id

    @property
    def service_date(self) -> date:
        return self._service_date

    @property
    def status(self) -> BlockAssignmentStatus:
        return self._status

    @property
    def observations(self) -> list[BusObservation]:
        """
        Returns a shallow copy of this list of bus observations.
        """
        return self._observations.copy()

    def _check_block_assignment(self) -> None:
        require_type(Bus, assigned_bus=self._bus)
        require_type(WinnipegBlockID, assigned_block=self._block_id)
        require_type(date, service_date=self._service_date)
        require_type(BlockAssignmentStatus, status=self._status)
        require_type(list, bus_observation_list=self._observations)
        for obs in self._observations:
            require_type(BusObservation, bus_observation_in_list=obs)

            require_state(
                obs.bus == self._bus,
                "The observation's bus should be the same as the block assignment's bus."
            )

        require_state(
            len(self._observations) >= 1,
            "There should be at least one bus observation for the block assignment."
        )

