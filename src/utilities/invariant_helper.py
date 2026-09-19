"""
Assertion functions used enforce preconditions, postconditions, and
class invariants.
"""

def require_not_none(obj, message: str) -> None:
    """
    Raises a ValueError with a given error message if the given object
    is None.
    """
    if obj is None:
        raise ValueError(message)

def require_state(condition: bool, message: str) -> None:
    """
    Raises a ValueError with a given error message if the given condition
    evaluates to False.
    """
    if not condition:
        raise ValueError(message)