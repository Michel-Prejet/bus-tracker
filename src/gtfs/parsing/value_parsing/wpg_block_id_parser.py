from gtfs.constants.gtfs_constants import WPG_BLOCK_ID_TOKEN_DELIMITER, WPG_BLOCK_ID_NUM_TOKENS
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID
from gtfs.exceptions.value_parsing_error import ValueParsingError
from gtfs.parsing.value_parsing.primitive_parser import parse_integer


def parse_winnipeg_block_id(raw: str) -> WinnipegBlockID:
    """
    Throws an exception if the given string is not a valid Winnipeg block ID;
    otherwise returns a WinnipegBlockID object.
    """
    raw = raw.strip()

    block_id_tokens = raw.split(WPG_BLOCK_ID_TOKEN_DELIMITER)

    if len(block_id_tokens) != WPG_BLOCK_ID_NUM_TOKENS:
        raise ValueParsingError

    for token in block_id_tokens:
        try:
            parse_integer(token)
        except ValueError as e:
            raise ValueParsingError from e

    return WinnipegBlockID(raw)