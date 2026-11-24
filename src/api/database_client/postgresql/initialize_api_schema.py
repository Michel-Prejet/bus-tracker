from pathlib import Path
from global_packages.database_connection import connection


DDL_FILE = (Path(__file__).resolve().parent.parent.parent.parent.parent
            / "databases" / "create_tables_api.ddl")

def initialize_api_schema() -> None:
    """
    Executes create table statements for the API database schema.
    """
    with connection() as db:
        with db.cursor() as cursor:
            ddl = DDL_FILE.read_text(encoding="utf-8")
            cursor.execute(ddl)