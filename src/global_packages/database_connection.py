import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def connection() -> psycopg.Connection:
    """
    Returns a database connection.
    """
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )
