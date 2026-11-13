from pathlib import Path
from database_connection import connection


DDL_FILE = (Path(__file__).resolve().parent.parent.parent.parent
            / "databases" / "create_tables_gtfs.ddl")

def initialize_gtfs_schema() -> None:
    """
    Executes create table statements for the GTFS database schema.
    """
    with connection() as db:
        with db.cursor() as cursor:
            ddl = DDL_FILE.read_text(encoding="utf-8")
            cursor.execute(ddl)