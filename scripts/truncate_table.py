import psycopg2
import os
import logging
import random
from dotenv import load_dotenv
from utils import connect_to_db
from utils import logging_setup
from utils import find_tables

load_dotenv()
logging_setup()


def truncate_random_table(conn):
    with conn.cursor() as cur:
        # Query to get all user-created tables in the public schema
        cur.execute(find_tables())
        tables = cur.fetchall()

        if not tables:
            logging.info("No tables found to truncate.")
            return

        # Randomly select one table from the list
        table_to_truncate = random.choice(tables)[0]
        cur.execute(f"TRUNCATE TABLE {table_to_truncate} RESTART IDENTITY CASCADE;")
        logging.info(f"Truncated table: {table_to_truncate}")

    conn.commit()


if __name__ == "__main__":
    conn = connect_to_db()
    truncate_random_table(conn)
    conn.close()
