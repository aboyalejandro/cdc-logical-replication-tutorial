import psycopg2
import os
import logging
import random
from dotenv import load_dotenv
from utils import connect_to_db
from utils import logging_setup

load_dotenv()
logging_setup()


def connect_to_db():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_SOURCE_DB_NAME"),
        user=os.getenv("POSTGRES_SOURCE_USER"),
        password=os.getenv("POSTGRES_SOURCE_PASSWORD"),
        host=os.getenv("POSTGRES_SOURCE_HOST"),
        port=5432,
    )


def truncate_random_table(conn):
    with conn.cursor() as cur:
        # Query to get all user-created tables in the public schema
        cur.execute(
            """
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """
        )
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
    logging.info("All specified tables have been truncated.")
