from invariant_helper import require_not_none, require_state


def require_valid_row_num(value: int) -> None:
    require_not_none(row_number=value)
    require_state(value >= 1, "Row number should be positive.")