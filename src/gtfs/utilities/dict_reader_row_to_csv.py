import csv
import io
from invariant_helper import require_not_none


def dict_reader_row_to_csv(row: dict[str | None, str]) -> str:
    """
    Converts the given DictReader row into a CSV string.
    """
    require_not_none(row=row)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=row.keys())

    writer.writerow(row)

    return output.getvalue().rstrip("\r\n")