from gtfs.domain.shape_point import ShapePoint
from utilities.invariant_helper import require_not_none, require_state, require_non_empty_str
from bisect import insort


class Shape:
    """
    Represents a geometric shape followed by a bus route as a series of
    points (coordinates in a sequence).
    """

    def __init__(self, shape_id: str):
        self._shape_id = shape_id
        self._points: list[ShapePoint] = []

        self._check_shape()

    @property
    def id(self) -> str:
        return self._shape_id

    @property
    def points(self) -> list[ShapePoint]:
        """
        Returns the list of points that make up this shape, sorted by
        strictly increasing sequence order.
        """
        return self._points.copy()

    def add_point(self, point: ShapePoint) -> None:
        """
        Adds a given point to this shape. A shape cannot contain two points
        with the same sequence order.
        """
        require_not_none(shape_point=point)
        for curr_point in self._points:
            require_state(
                point.sequence_order != curr_point.sequence_order,
                "There cannot be two points in the same shape with the same sequence order."
            )

        insort(self._points, point)

        self._check_shape()

    def _check_shape(self) -> None:
        require_not_none(
            shape_id=self._shape_id,
            shape_point_list=self._points
        )

        require_non_empty_str(
            shape_id=self._shape_id
        )

        prev: ShapePoint | None = None
        for point in self._points:
            require_not_none(
                shape_point_in_list=point
            )

            if prev is not None:
                require_state(
                    prev.sequence_order < point.sequence_order,
                    "Shape point list should be sorted by strictly increasing sequence order values."
                )
            prev = point