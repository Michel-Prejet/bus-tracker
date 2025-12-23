class Ride:
    """
    Represents a bus ride with a unique date and boarding time. Stores the route number, the bus's tracking number,
    the bus's destination, the block number, and any additional notes (can be blank).
    """

    def __init__(self, date, boarding_time, tracking_number, route, destination, block_number, notes):
        """
        Creates a new instance.

        :param date: the date of the ride to construct.
        :param boarding_time: the boarding time of the ride to construct.
        :param tracking_number: the 3-digit tracking number of the bus that was ridden.
        :param route: the route that was taken.
        :param destination: the destination of the route.
        :param block_number: the number of the block containing the bus's current trip.
        :param notes: any additional notes relevant to the ride (can be blank).
        """
        self.date = date
        self.boarding_time = boarding_time
        self.tracking_number = tracking_number
        self.route = route
        self.destination = destination
        self.block_number = block_number
        self.notes = notes

    def __eq__(self, other):
        """
        Determines whether `other` is an instance of Ride with the same date and boarding time as `self`.

        :param other: the object to check for equality.
        :return: True if `other` is an instance of ride with the same date and boarding time as `self`.
        """
        if isinstance(other, Ride):
            return self.date == other.date and self.boarding_time == other.boarding_time

        return False
