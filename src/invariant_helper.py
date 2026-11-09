"""
Assertion functions used to enforce preconditions, postconditions, and
class invariants.
"""
from types import UnionType
from typing import get_args, Callable


def require_not_none(**objs: object) -> None:
    """
    Raises an AssertionError if any of the given objects are None. Uses the
    corresponding keyword argument name in the error message.
    """
    for name, obj in objs.items():
        if obj is None:
            raise AssertionError(
                f"{name.replace('_', ' ').capitalize()} "
                f"should not be None."
            )

def require_type(expected_type: type | UnionType, **objs: object) -> None:
    """
    Raises an AssertionError if any of the given objects are not of the expected
    type. Uses the corresponding keyword argument name in the error message.
    """
    allowed_types = (
        get_args(expected_type)
        if isinstance(expected_type, UnionType)
        else (expected_type,)
    )

    for name, obj in objs.items():
        if type(obj) not in allowed_types:
            raise AssertionError(
                f"{name.replace('_', ' ').capitalize()} "
                f"of type {type(obj).__name__} should be of type "
                f"{' | '.join(t.__name__ for t in allowed_types)}."
            )

def require_state(condition: bool, message: str) -> None:
    """
    Raises an AssertionError with a given error message if the given condition
    evaluates to False.
    """
    if not condition:
        raise AssertionError(message)

def require_non_empty_str(**strings: str) -> None:
    """
    Raises an AssertionError if any of the given strings are empty or only
    whitespace. Uses the corresponding keyword argument name in the error
    message.
    """
    for name, string in strings.items():
        if len(string.strip()) == 0:
            raise AssertionError(
                f"{name.replace('_', ' ').capitalize()} should "
                f"not be empty or only whitespace."
            )

def require_not_throws(**function_calls: Callable) -> None:
    """
    Throws an AssertionError if any of the given function calls throw an
    exception. Uses the corresponding keyword argument name in the error
    message.
    """
    for name, call in function_calls.items():
        try:
            call()
        except Exception as e:
            raise AssertionError(
                f"{name.replace('_', ' ').capitalize()} should not have "
                f"thrown {type(e).__name__}."
            ) from e
