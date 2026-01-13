class RideManagerError(Exception):
    """
    Exception thrown when any ride-related logic error occurs.
    """
    pass

class DateRangeError(RideManagerError):
    pass

class RideFilterError(RideManagerError):
    pass