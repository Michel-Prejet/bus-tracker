from utilities.invariant_helper import require_not_none, require_state
import pycountry
from decimal import Decimal


class FareCost:
    """
    Enforces validity on the price and the currency code for a fare attribute.
    """

    def __init__(self, price: Decimal, currency_code: str):
        self._price = price
        self._currency_code = currency_code

        self._check_fare_cost()

    @property
    def price(self) -> Decimal:
        return self._price

    @property
    def currency_code(self) -> str:
        return self._currency_code

    def _check_fare_cost(self) -> None:
        require_not_none(
            fare_price=self._price,
            fare_currency_code=self._currency_code
        )

        require_state(
            self._price >= 0,
            "Fare price should be non-negative."
        )

        require_state(
            pycountry.currencies.get(alpha_3=self._currency_code) is not None,
            f"{self._currency_code} is not a valid ISO 4217 currency code."
        )