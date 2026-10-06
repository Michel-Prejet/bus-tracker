from datetime import timedelta
from gtfs.domain.enums.fare_payment_method import FarePaymentMethod
from gtfs.domain.enums.num_transfers import NumTransfers
from gtfs.domain.values.fare_cost import FareCost
from utilities.invariant_helper import require_not_none, require_non_empty_str, require_state


class FareAttribute:
    """
    Represents a fare attribute associated with routes in a transit agency.
    Stores an ID, a price and currency, a payment method, transfer information,
    and the agency ID.
    """

    def __init__(
            self,
            fare_id: str,
            cost: FareCost,
            payment_method: FarePaymentMethod,
            num_transfers: NumTransfers,
            transfer_duration: timedelta | None,
            agency_id: str | None
    ):
        self._fare_id = fare_id
        self._cost = cost
        self._payment_method = payment_method
        self._num_transfers = num_transfers
        self._transfer_duration = transfer_duration
        self._agency_id = agency_id

        self._check_fare_attribute()

    @property
    def id(self) -> str:
        return self._fare_id

    @property
    def cost(self) -> FareCost:
        return self._cost

    @property
    def payment_method(self) -> FarePaymentMethod:
        return self._payment_method

    @property
    def num_transfers(self) -> NumTransfers:
        return self._num_transfers

    @property
    def transfer_duration(self) -> timedelta | None:
        return self._transfer_duration

    @property
    def agency_id(self) -> str | None:
        return self._agency_id

    def _check_fare_attribute(self) -> None:
        require_not_none(
            fare_id=self._fare_id,
            fare_cost=self._cost,
            fare_payment_method=self._payment_method,
            number_of_transfers=self._num_transfers
        )

        require_non_empty_str(fare_id=self._fare_id)
        if self._agency_id is not None:
            require_non_empty_str(agency_id=self._agency_id)

        if self._transfer_duration is not None:
            require_state(
                self._transfer_duration >= timedelta(seconds=0),
                "Transfer duration should be non-negative."
            )