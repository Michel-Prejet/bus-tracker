from datetime import date, time

from utilities.InvariantHelper import require_not_none, require_state

class Ride:
    """
    Represents a bus ride with a unique date and boarding time. Stores the route number, the bus's tracking number,
    the bus's destination, the block number, and any additional notes (can be blank).
    """

    TRACKING_NUMBER_LENGTH = 3

    def __init__(self, ride_date: date, boarding_time: time, route: str, tracking_number: str,
                 destination: str, block_number: str, notes: str):
        """
        Creates a new instance of Ride.

        :param ride_date: the date of the ride to construct.
        :param boarding_time: the boarding time of the ride to construct.
        :param route: the route that was taken.
        :param tracking_number: the 3-digit tracking number of the bus that was ridden.
        :param destination: the destination of the route.
        :param block_number: the number of the block containing the bus's current trip.
        :param notes: any additional notes relevant to the ride (can be blank).
        """
        require_not_none(ride_date,"Date should not be None.")
        require_not_none(boarding_time, "Boarding time should not be None.")
        require_not_none(route, "Route should not be None.")
        require_not_none(tracking_number, "Tracking number should not be None.")
        require_not_none(destination, "Destination should not be None.")
        require_not_none(block_number, "Block number should not be None.")
        require_not_none(notes, "Notes should not be None.")
        require_state(isinstance(ride_date, date), "Ride date should be a date object.")
        require_state(isinstance(boarding_time, time), "Boarding time should be a time object.")

        self.ride_date: date = ride_date
        self.boarding_time: time = boarding_time
        self.route: str = route
        self.tracking_number: str = tracking_number
        self.destination: str = destination
        self.block_number: str = block_number
        self.notes: str = notes

        self._check_ride()

    def __eq__(self, other) -> bool:
        """
        Determines whether `other` is an instance of Ride with the same date and boarding time as `self`.

        :param other: the object to check for equality.
        :return: True if `other` is an instance of ride with the same date and boarding time as `self`; False
        otherwise.
        """
        if isinstance(other, Ride):
            return self.ride_date == other.ride_date and self.boarding_time == other.boarding_time

        return False

    def _check_ride(self) -> None:
        require_not_none(self.ride_date, "Date should not be None.")
        require_not_none(self.boarding_time, "Boarding time should not be None.")
        require_not_none(self.tracking_number, "Tracking number should not be None.")
        require_state(len(self.tracking_number) == self.TRACKING_NUMBER_LENGTH,
                      "Tracking number length should be 3.")
        require_state(self.tracking_number.isdigit(), "Tracking number should only contain digits.")
        require_not_none(self.route, "Route should not be None.")
        require_state(len(self.route) >= 1, "Route should not be empty.")
        require_not_none(self.destination, "Destination should not be None.")
        require_state(len(self.destination) >= 1, "Destination should not be empty.")
        require_not_none(self.block_number, "Block number should not be None.")
        require_state(len(self.block_number) >= 1, "Block number should not be empty.")
        require_not_none(self.notes, "Notes should not be None.")

