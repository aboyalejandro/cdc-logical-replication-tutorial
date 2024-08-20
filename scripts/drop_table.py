import psycopg2
import logging
import random
from dotenv import load_dotenv
from utils import connect_to_db
from utils import logging_setup

load_dotenv()
logging_setup()


def drop_random_table(conn):
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
            logging.info("No tables found to drop.")
            return

        # Randomly select one table from the list
        table_to_drop = random.choice(tables)[0]
        cur.execute(f"DROP TABLE IF EXISTS {table_to_drop} CASCADE;")
        logging.info(f"Dropped table: {table_to_drop}")

    conn.commit()


if __name__ == "__main__":
    conn = connect_to_db()
    drop_random_table(conn)
    conn.close()
    logging.info("All specified tables have been dropped.")
