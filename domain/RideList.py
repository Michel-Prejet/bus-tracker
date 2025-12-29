from utilities.InvariantHelper import require_not_none

class RideList:
    """
    Represents a list of rides with basic add, contains, get, and remove methods. Does not allow duplicates.
    """
    def __init__(self):
        """
        Creates a new instance of RideList with an empty list of rides.
        """
        self.rides = []

        self._check_ride_list()

    def add_ride(self, ride):
        """
        Adds a given ride to this ride list, or takes no action if a ride with the same
        date/time already exists.

        :param ride: the ride to add to this ride list.
        """
        require_not_none(ride, "Ride should not be None.")

        if not ride in self.rides:
            self.rides.append(ride)

        self._check_ride_list()

    def get_ride(self, date, time):
        """
        Retrieves a ride from this ride list with a given date and boarding time.

        :param date: the date of the ride to retrieve.
        :param time: the boarding time of the ride to retrieve.
        :return: the ride in this ride list corresponding to `date` and `time`, or `None` if no such ride exists.
        """
        require_not_none(date, "Date should not be None.")
        require_not_none(time, "Time should not be None.")

        for curr in self.rides:
            if curr.date == date and curr.boarding_time == time:
                return curr

        return None

    def get_rides_on_bus(self, tracking_number):
        """
        Retrieves all rides from this ride list on a bus with a given tracking
        number.

        :param tracking_number: the 3-digit tracking number of the bus for which
        to retrieve all rides.
        :return: a list containing all rides on bus `tracking_number`.
        """
        rides_on_bus = []

        for curr in self.rides:
            if curr.tracking_number == tracking_number:
                rides_on_bus.append(curr)

        return rides_on_bus

    def remove_ride(self, date, time):
        """
        Removes a ride with a given date and boarding time from this ride list, or takes
        no action if no such ride exists.

        :param date: the date of the ride to remove.
        :param time: the boarding time of the ride to remove.
        """
        require_not_none(date, "Date should not be None.")
        require_not_none(time, "Time should not be None.")

        ride = self.get_ride(date, time)
        if ride is not None:
            self.rides.remove(ride)

        self._check_ride_list()

    def _check_ride_list(self):
        require_not_none(self.rides, "Ride list should not be None.")
        for ride in self.rides:
            require_not_none(ride, "Ride in ride list should not be None.")

