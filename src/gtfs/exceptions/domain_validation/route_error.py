"""
Family of exceptions thrown whenever a route is constructed from invalid
attributes.
"""
from utilities.invariant_helper import require_not_none, require_state, require_non_empty_str


class RouteError(Exception):
    pass

class RouteAttributeError(RouteError):
    def __init__(self, row_num: int):
        require_not_none(row_number=row_num)
        require_state(row_num >= 0, "Row number should not be negative.")

        self._row_num = row_num

    @property
    def row_num(self) -> int:
        return self._row_num

class EmptyRouteIdError(RouteAttributeError):
    pass

class InvalidRouteTypeError(RouteAttributeError):
    pass

class InvalidRouteUrlError(RouteAttributeError):
    pass

class InvalidRouteBackgroundColourError(RouteAttributeError):
    pass

class InvalidRouteTextColourError(RouteAttributeError):
    pass

class InvalidRouteSortOrderError(RouteAttributeError):
    pass

class MissingRouteNameError(RouteAttributeError):
    """
    Thrown when BOTH the short and long route names are None.
    """
    pass

class DuplicateRouteIdError(RouteError):
    def __init__(self, duplicated_route_id: str):
        require_not_none(route_id=duplicated_route_id)
        require_non_empty_str(route_id=duplicated_route_id)

        self._duplicated_route_id = duplicated_route_id

    @property
    def duplicated_route_id(self) -> str:
        return self._duplicated_route_id
