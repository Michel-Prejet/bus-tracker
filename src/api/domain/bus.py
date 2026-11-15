from api.api_constants import MIN_YEAR
from api.domain.enums.bus_length import BusLength
from api.domain.enums.propulsion_type import PropulsionType
from invariant_helper import require_type, require_non_empty_str, require_state


class Bus:
    """
    Represents a bus in Winnipeg Transit's fleet with a tracking number.
    Includes optional details about the model, manufacturer, year, propulsion
    type, and length of the bus.
    """

    def __init__(
            self,
            tracking_number: str,
            model: str | None = None,
            manufacturer: str | None = None,
            year: int | None = None,
            propulsion_type: PropulsionType | None = None,
            length: BusLength | None = None,
            retired: bool = False
    ):
        self._tracking_number = tracking_number
        self._model = model
        self._manufacturer = manufacturer
        self._year = year
        self._propulsion_type = propulsion_type
        self._length = length
        self._retired = retired

        self._check_bus()

    def __eq__(self, other) -> bool:
        """
        Returns True if the given object is an instance of Bus with the same
        tracking number as this instance.
        """
        return (
            isinstance(other, Bus) and
            self._tracking_number == other.tracking_number
        )

    @property
    def tracking_number(self) -> str:
        return self._tracking_number

    @property
    def model(self) -> str | None:
        return self._model

    @property
    def manufacturer(self) -> str | None:
        return self._manufacturer

    @property
    def year(self) -> int | None:
        return self._year

    @property
    def propulsion_type(self) -> PropulsionType | None:
        return self._propulsion_type

    @property
    def length(self) -> BusLength | None:
        return self._length

    @property
    def retired(self) -> bool:
        return self._retired

    def _check_bus(self) -> None:
        require_type(str, bus_tracking_number=self._tracking_number)
        require_type(
            str | None,
            model=self._model,
            manufacturer=self._manufacturer
        )
        require_type(int | None, year=self._year)
        require_type(
            PropulsionType | None,
            propulsion_type=self._propulsion_type
        )
        require_type(BusLength | None, length=self._length)
        require_type(bool, retired_status=self._retired)

        require_non_empty_str(bus_tracking_number=self._tracking_number)

        if self._model is not None:
            require_non_empty_str(model=self._model)

        if self._manufacturer is not None:
            require_non_empty_str(manufacturer=self._manufacturer)

        if self._year is not None:
            require_state(
                self._year >= MIN_YEAR,
                f"Bus year should be greater than or equal to {MIN_YEAR}."
            )