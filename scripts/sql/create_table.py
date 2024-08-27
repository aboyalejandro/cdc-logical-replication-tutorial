import psycopg2
import logging
from utils import connect_to_db
from utils import logging_setup

logging_setup()


def create_random_table(conn):
    with conn.cursor() as cur:
        tables = {
            "stores": """
                CREATE TABLE IF NOT EXISTS stores (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
            """,
            "vendors": """
                CREATE TABLE IF NOT EXISTS vendors (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
            """,
            "resellers": """
                CREATE TABLE IF NOT EXISTS resellers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
            """,
        }

        # Pick a random table that doesn't exist in the database
        for table_name in list(tables.keys()):
            cur.execute(
                f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}');"
            )
            if not cur.fetchone()[0]:
                cur.execute(tables[table_name])
                logging.info(f"Created table: {table_name}")
                break  # Exit after creating one table
    conn.commit()


if __name__ == "__main__":
    conn = connect_to_db("SOURCE")
    create_random_table(conn)
    conn.close()
    logging.info("Random table creation complete.")
