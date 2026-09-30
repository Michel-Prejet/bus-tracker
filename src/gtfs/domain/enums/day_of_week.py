from datetime import date
from enum import Enum
from utilities.invariant_helper import require_not_none


class DayOfWeek(Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

    @staticmethod
    def from_date(date_obj: date) -> "DayOfWeek":
        """
        Returns the day of the week corresponding to the given date as a
        DayOfWeek object.
        """
        require_not_none(
            date=date_obj
        )

        return DayOfWeek(date_obj.weekday())