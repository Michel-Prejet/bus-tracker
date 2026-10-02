from gtfs.domain.values.coordinates import Coordinates
from utilities.invariant_helper import require_not_none, require_state


class ShapePoint:
    """
    Represents a single point on a geometric shape representing the path taken
    by a bus route. Contains a set of coordinates and the order in which this
    point should appear in the sequence making up the shape.
    """

    def __init__(self, coordinates: Coordinates, sequence_order: int):
        self._coordinates = coordinates
        self._sequence_order = sequence_order

        self._check_shape_point()

    def __lt__(self, other):
        """
        Returns True if this shape point's sequence order is less than the
        given shape point's sequence order; returns False otherwise.
        """
        if not isinstance(other, ShapePoint):
            return NotImplemented

        return self._sequence_order < other.sequence_order

    @property
    def coordinates(self) -> Coordinates:
        return self._coordinates

    @property
    def sequence_order(self) -> int:
        return self._sequence_order

    def _check_shape_point(self) -> None:
        require_not_none(
            shape_point_coordinates=self._coordinates,
            shape_point_sequence_order=self._sequence_order,
        )

        require_state(
            self._sequence_order >= 0,
            "Shape point sequence order should be non-negative."
        )