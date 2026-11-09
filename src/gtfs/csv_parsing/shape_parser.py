from gtfs.constants.csv_column_headers.shapes_headers import SHAPE_ID_COL_HEADER, SHAPE_POINT_LATITUDE_COL_HEADER, \
    SHAPE_POINT_LONGITUDE_COL_HEADER, SHAPE_POINT_SEQUENCE_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import parse_gtfs_file
from gtfs.domain.shape.shape import Shape
from gtfs.domain.shape.shape_point import ShapePoint
from gtfs.domain.values.coordinates import Coordinates
from gtfs.validation.shape_validator import validate_and_parse_shape_id, validate_and_parse_shape_point_latitude, \
    validate_and_parse_shape_point_sequence_order, \
    validate_and_parse_shape_point_longitude, validate_shape_point_collection


SHAPE_REQUIRED_COLUMNS = [
    SHAPE_ID_COL_HEADER,
    SHAPE_POINT_LATITUDE_COL_HEADER,
    SHAPE_POINT_LONGITUDE_COL_HEADER,
    SHAPE_POINT_SEQUENCE_COL_HEADER
]

def parse_shapes(file_name: str) -> dict[str, Shape]:
    """
    Creates a dictionary of Shape objects (keyed by shape ID), composed of the
    Shape Point objects constructed from the rows in the given file, or throws
    an exception if the file or its contents are invalid.
    """
    shape_points = parse_gtfs_file(
        file_name=file_name,
        required_column_names=SHAPE_REQUIRED_COLUMNS,
        object_builder_from_row=_create_shape_point_from_row
    )

    shape_point_dict = _create_shape_point_dict_from_tuples(shape_points)

    validate_shape_point_collection(shape_point_dict)

    shapes = _create_shape_list_from_shape_point_dict(shape_point_dict)

    return {shape.id: shape for shape in shapes}

def _create_shape_point_from_row(
        row: dict[str, str | None],
        row_num: int
) -> tuple[str, ShapePoint]:
    shape_id = validate_and_parse_shape_id(row[SHAPE_ID_COL_HEADER], row_num)

    coordinates = Coordinates(
        validate_and_parse_shape_point_latitude(
            row[SHAPE_POINT_LATITUDE_COL_HEADER], row_num
        ),
        validate_and_parse_shape_point_longitude(
            row[SHAPE_POINT_LONGITUDE_COL_HEADER], row_num
        )
    )

    sequence_order = validate_and_parse_shape_point_sequence_order(
        row[SHAPE_POINT_SEQUENCE_COL_HEADER], row_num
    )

    return shape_id, ShapePoint(coordinates, sequence_order)

def _create_shape_point_dict_from_tuples(
        shape_points: list[tuple[str, ShapePoint]]
) -> dict[str, list[ShapePoint]]:
    """
    Creates a dictionary mapping shape IDs to a list of their corresponding
    shape points, given a list of (shapeID, shapePoint) tuples.
    """
    shape_point_dict: dict[str, list[ShapePoint]] = {}
    for shape_id, shape_pt in shape_points:
        if shape_id not in shape_point_dict:
            shape_point_dict[shape_id] = []

        shape_point_dict[shape_id].append(shape_pt)

    return shape_point_dict

def _create_shape_list_from_shape_point_dict(
        shape_point_dict: dict[str, list[ShapePoint]]
) -> list[Shape]:
    """
    Constructs a list of shapes using the given dictionary mapping shape
    IDs to a list of their corresponding shape points.
    """
    shapes: list[Shape] = []
    for shape_id, points in shape_point_dict.items():
        shape = Shape(shape_id)

        for point in points:
            shape.add_point(point)

        shapes.append(shape)

    return shapes
