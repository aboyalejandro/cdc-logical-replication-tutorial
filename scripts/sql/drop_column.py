import psycopg2
import random
import logging
from utils import connect_to_db, logging_setup, find_tables

logging_setup()


def drop_column_from_random_table(conn):
    with conn.cursor() as cur:
        # Query to get all user-created tables in the public schema
        cur.execute(find_tables())
        tables = cur.fetchall()

        if not tables:
            logging.info("No tables found to drop a column.")
            return

        # Randomly select one table from the list
        table_to_alter = random.choice(tables)[0]

        # Check if the "subtype" column exists
        cur.execute(
            f"""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = '{table_to_alter}' AND column_name = 'subtype';
        """
        )
        column_exists = cur.fetchone()

        if column_exists:
            # Drop the 'subtype' column from the selected table
            cur.execute(f"ALTER TABLE {table_to_alter} DROP COLUMN subtype;")
            logging.info(f"Dropped column 'subtype' from table: {table_to_alter}")
        else:
            logging.info(f"Column 'subtype' does not exist in table: {table_to_alter}")

    conn.commit()


if __name__ == "__main__":
    conn = connect_to_db("SOURCE")
    drop_column_from_random_table(conn)
    conn.close()
