from domain.exceptions.EmptyBlockNumberError import EmptyBlockNumberError
from domain.exceptions.EmptyDestinationError import EmptyDestinationError
from domain.exceptions.EmptyRouteError import EmptyRouteError
from domain.exceptions.InvalidBlockNumberError import InvalidBlockNumberError
from domain.exceptions.TrackingNumberDigitError import TrackingNumberDigitError
from domain.exceptions.TrackingNumberLengthError import TrackingNumberLengthError
from utilities.InvariantHelper import require_not_none, require_state
import datetime

class Ride:
    """
    Represents a bus ride with a unique date and boarding time. Stores the route number, the bus's tracking number,
    the bus's destination, the block number, and any additional notes (can be blank).
    """

    TRACKING_NUMBER_LENGTH = 3

    def __init__(self, ride_date, boarding_time, tracking_number, route, destination, block_number, notes):
        """
        Creates a new instance of Ride.

        :param ride_date: the date of the ride to construct.
        :param boarding_time: the boarding time of the ride to construct.
        :param tracking_number: the 3-digit tracking number of the bus that was ridden.
        :param route: the route that was taken.
        :param destination: the destination of the route.
        :param block_number: the number of the block containing the bus's current trip.
        :param notes: any additional notes relevant to the ride (can be blank).
        """
        self.ride_date = ride_date
        self.boarding_time = boarding_time
        self.tracking_number = tracking_number
        self.route = route
        self.destination = destination
        self.block_number = block_number
        self.notes = notes

        self._check_ride()

    @classmethod
    def build(cls, ride_date, boarding_time, tracking_number, route, destination, block_number, notes):
        """
        Creates a new instance of Ride using the given arguments, or raises an exception if any of the
        arguments are invalid.

        :param ride_date: the date of the ride to construct.
        :param boarding_time: the boarding time of the ride to construct.
        :param tracking_number: the 3-digit tracking number of the bus that was ridden.
        :param route: the route that was taken.
        :param destination: the destination of the route.
        :param block_number: the number of the block containing the bus's current trip.
        :param notes: any additional notes relevant to the ride (can be blank).
        :return: an instance of Ride created with the given parameters.
        """
        require_not_none(ride_date,"Date should not be None.")
        require_not_none(boarding_time, "Boarding time should not be None.")
        require_not_none(tracking_number, "Tracking number should not be None.")
        require_not_none(route, "Route should not be None.")
        require_not_none(destination, "Destination should not be None.")
        require_not_none(block_number, "Block number should not be None.")
        require_not_none(notes, "Notes should not be None.")
        require_state(isinstance(ride_date, datetime.date), "Ride date should be a date object.")
        require_state(isinstance(boarding_time, datetime.time), "Boarding time should be a time object.")

        tracking_number = tracking_number.strip()
        route = route.strip()
        destination = destination.strip()
        block_number = block_number.strip()
        notes = notes.strip()

        if not tracking_number.isdigit():
            raise TrackingNumberDigitError()

        if len(tracking_number) != cls.TRACKING_NUMBER_LENGTH:
            raise TrackingNumberLengthError()

        if not route:
            raise EmptyRouteError()

        if not destination:
            raise EmptyDestinationError()

        if not block_number:
            raise EmptyBlockNumberError()

        for char in block_number:
            if not char.isdigit() and char != "-":
                raise InvalidBlockNumberError()

        if block_number.count("-") != 1:
            raise InvalidBlockNumberError()

        if not 0 < block_number.find("-") < len(block_number) - 1:
            raise InvalidBlockNumberError()

        return cls(ride_date, boarding_time, tracking_number, route, destination, block_number, notes)

    def __eq__(self, other):
        """
        Determines whether `other` is an instance of Ride with the same date and boarding time as `self`.

        :param other: the object to check for equality.
        :return: True if `other` is an instance of ride with the same date and boarding time as `self`; False
        otherwise.
        """
        if isinstance(other, Ride):
            return self.ride_date == other.ride_date and self.boarding_time == other.boarding_time

        return False

    def _check_ride(self):
        require_not_none(self.ride_date, "Date should not be None.")
        require_not_none(self.boarding_time, "Boarding time should not be None.")
        require_not_none(self.tracking_number, "Tracking number should not be None.")
        require_state(len(self.tracking_number) == self.TRACKING_NUMBER_LENGTH, "Tracking number length should be 3.")
        require_state(self.tracking_number.isdigit(), "Tracking number should only contain digits.")
        require_not_none(self.route, "Route should not be None.")
        require_state(len(self.route) >= 1, "Route should not be empty.")
        require_not_none(self.destination, "Destination should not be None.")
        require_state(len(self.destination) >= 1, "Destination should not be empty.")
        require_not_none(self.block_number, "Block number should not be None.")
        require_state(len(self.block_number) >= 1, "Block number should not be empty.")
        require_not_none(self.notes, "Notes should not be None.")

