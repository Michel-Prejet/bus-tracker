class RideError(Exception):
    """
    Exception thrown when any given ride attributes are invalid.
    """
    pass

class InvalidDateError(RideError):
    pass

class InvalidTimeError(RideError):
    pass

class EmptyRouteError(RideError):
    pass

class TrackingNumberDigitError(RideError):
    pass

class TrackingNumberLengthError(RideError):
    pass

class EmptyDestinationError(RideError):
    pass

class EmptyBlockNumberError(RideError):
    pass

class InvalidBlockNumberError(RideError):
    pass