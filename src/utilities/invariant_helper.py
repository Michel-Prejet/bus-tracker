"""
Assertion functions used enforce preconditions, postconditions, and
class invariants.
"""

def require_not_none(**objs: object) -> None:
    """
    Raises a ValueError if any of the given objects are None. Uses the
    corresponding keyword argument name in the error message.
    """
    for name, obj in objs.items():
        if obj is None:
            raise ValueError(f"{name.replace('_', ' ').capitalize()} should not be None.")

def require_state(condition: bool, message: str) -> None:
    """
    Raises a ValueError with a given error message if the given condition
    evaluates to False.
    """
    if not condition:
        raise ValueError(message)

def require_non_empty_str(**strings: str) -> None:
    """
    Raises a ValueError if any of the given strings are empty or only
    whitespace. Uses the corresponding keyword argument name in the error
    message.
    """
    for name, string in strings.items():
        if len(string.strip()) == 0:
            raise ValueError(
                f"{name.replace('_', ' ').capitalize()} should "
                f"not be empty or only whitespace."
            )
