from gtfs.constants.csv_column_headers.shapes_headers import SHAPE_ID_COL_HEADER, SHAPE_POINT_LATITUDE_COL_HEADER, \
    SHAPE_POINT_LONGITUDE_COL_HEADER, SHAPE_POINT_SEQUENCE_COL_HEADER
from gtfs.constants.gtfs_constants import SHAPES_FILE_NAME
from gtfs.domain.shape.shape_point import ShapePoint
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_row_error import GTFSAttributeError
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.general_validator import validate_and_parse_nonempty_str, validate_and_parse_latitude, \
    validate_and_parse_longitude, validate_and_parse_integer_str, assert_that_elements_are_unique
from invariant_helper import require_not_none


def validate_shape_point_collection(shapes: dict[str, list[ShapePoint]]) -> None:
    """
    Throws an exception if the same sequence order appears more than once in
    any of the lists of shape points in the given dictionary.
    """
    require_not_none(shape_list=shapes)
    for shape in shapes:
        require_not_none(shape_in_list=shape)

    try:
        for shape_pt_list in shapes.values():
            assert_that_elements_are_unique(
                [str(shape_pt.sequence_order) for shape_pt in shape_pt_list]
            )
    except ValueError as e:
        raise GTFSCollectionError(
            file_name=SHAPES_FILE_NAME,
            names_of_columns_with_violated_restrictions=[SHAPE_POINT_SEQUENCE_COL_HEADER]
        ) from e

def validate_and_parse_shape_id(raw: str, row_num: int) -> str:
    """
    Throws an exception if the given string is empty or only whitespace;
    otherwise returns the trimmed string.
    """
    require_not_none(raw_shape_id=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SHAPES_FILE_NAME,
            column_name=SHAPE_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_shape_point_latitude(raw: str, row_num: int) -> float:
    """
    Throws an exception if the given string is not a floating-point value between
    -90 and 90 (inclusive); returns a float otherwise.
    """
    require_not_none(raw_shape_point_latitude=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_latitude(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SHAPES_FILE_NAME,
            column_name=SHAPE_POINT_LATITUDE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_shape_point_longitude(raw: str, row_num: int) -> float:
    """
    Throws an exception if the given string is not a floating-point value between
    -180 and 180 (inclusive); returns a float otherwise.
    """
    require_not_none(raw_shape_point_longitude=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_longitude(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SHAPES_FILE_NAME,
            column_name=SHAPE_POINT_LONGITUDE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_shape_point_sequence_order(raw: str, row_num: int) -> int:
    """
    Throws an exception if the given string does not correspond to a valid
    non-negative GTFS integer value; otherwise returns the value as an integer.
    """
    require_not_none(raw_shape_point_sequence_value=raw)
    require_valid_row_num(row_num)

    try:
        shape_point_sequence = validate_and_parse_integer_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SHAPES_FILE_NAME,
            column_name=SHAPE_POINT_SEQUENCE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

    if shape_point_sequence < 0:
        raise GTFSAttributeError(
            file_name=SHAPES_FILE_NAME,
            column_name=SHAPE_POINT_SEQUENCE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        )

    return shape_point_sequence