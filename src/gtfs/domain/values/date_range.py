from datetime import date
from utilities.invariant_helper import require_not_none, require_state


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
        require_not_none(
            date=date_obj
        )
        require_state(
            type(date_obj) is date,
            "Date should be a date object (not datetime)."
        )

        return self._start <= date_obj <= self._end

    def _check_date_range(self) -> None:
        require_not_none(
            start_date=self._start,
            end_date=self._end
        )

        require_state(
            type(self._start) is date,
            "Start date should be a date object (not datetime)."
        )
        require_state(
            type(self._end) is date,
            "End date should be a date object (not datetime)."
        )

        require_state(
            self._start <= self._end,
            "Start date should not be after the end date."
        )