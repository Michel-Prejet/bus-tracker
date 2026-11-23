from api.api_constants import MIN_YEAR
from api.domain.enums.bus_length import BusLength
from api.domain.enums.bus_propulsion_type import BusPropulsionType
from api.domain.enums.bus_status import BusStatus
from global_packages.utilities.invariant_helper import require_type, require_non_empty_str, require_state


class Bus:
    """
    Stores detailed information for a bus in Winnipeg Transit's fleet.
    """

    def __init__(
        self,
        tracking_number: str,
        year: int | None,
        model: str | None,
        manufacturer: str | None,
        length: BusLength | None,
        propulsion: BusPropulsionType | None,
        status: BusStatus = BusStatus.ACTIVE
    ):
        self._tracking_number = tracking_number
        self._year = year
        self._model = model
        self._manufacturer = manufacturer
        self._length = length
        self._propulsion = propulsion
        self._status = status

        self._check_bus()

    @property
    def tracking_number(self) -> str:
        return self._tracking_number

    @property
    def year(self) -> int | None:
        return self._year

    @property
    def model(self) -> str | None:
        return self._model

    @property
    def manufacturer(self) -> str | None:
        return self._manufacturer

    @property
    def length(self) -> BusLength | None:
        return self._length

    @property
    def propulsion(self) -> BusPropulsionType | None:
        return self._propulsion

    @property
    def status(self) -> BusStatus:
        return self._status

    def _check_bus(self) -> None:
        require_type(str, bus_tracking_num=self._tracking_number)
        require_type(int | None, bus_year=self._year)
        require_type(
            str | None,
            bus_model=self._model,
            bus_manufacturer=self._manufacturer
        )
        require_type(BusLength | None, bus_length=self._length)
        require_type(BusPropulsionType | None, bus_propulsion_type=self._propulsion)
        require_type(BusStatus, bus_status=self._status)

        require_non_empty_str(bus_tracking_num=self._tracking_number)

        if self._model is not None:
            require_non_empty_str(bus_model=self._model)

        if self._manufacturer is not None:
            require_non_empty_str(bus_manufacturer=self._manufacturer)

        require_state(
            self._year >= MIN_YEAR,
            f"Bus year should be greater than or equal to {MIN_YEAR}."
        )