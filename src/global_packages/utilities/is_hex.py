from gtfs.constants.gtfs_constants import HEX_COLOUR_BASE


def is_hex(colour: str) -> bool:
    """
    Returns True if the trimmed string only consists of hexadecimal characters,
    returns False otherwise.
    """
    try:
        int(colour, HEX_COLOUR_BASE)
        return True
    except ValueError:
        return False