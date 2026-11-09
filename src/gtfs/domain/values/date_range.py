from datetime import date
from invariant_helper import require_state, require_type


class DateRange:
    """
    A date range represented by a start date and an end date (both inclusive).
    """

    def __init__(self, start_date: date, end_date: date):
        self._start = start_date
        self._end = end_date

        self._check_date_range()

    @property
    def start(self) -> date:
        return self._start

    @property
    def end(self) -> date:
        return self._end

    def __contains__(self, date_obj: date) -> bool:
        """
        Returns True if the given date object is greater than or equal to this
        start date and less than or equal to this end date; returns False
        otherwise.
        """
        return self._start <= date_obj <= self._end

    def _check_date_range(self) -> None:
        require_type(date, start_date=self._start)
        require_type(date, end_date=self._end)

        require_state(
            self._start <= self._end,
            "Start date should not be after the end date."
        )