import psycopg2
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def connect_to_db():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_SOURCE_DB_NAME"),
        user=os.getenv("POSTGRES_SOURCE_USER"),
        password=os.getenv("POSTGRES_SOURCE_PASSWORD"),
        host=os.getenv("POSTGRES_SOURCE_HOST"),
        port=5432,
    )


def delete_products(conn, num_records):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM products WHERE product_id IN (SELECT product_id FROM products ORDER BY RANDOM() LIMIT %s)",
            (num_records,),
        )
    conn.commit()


def delete_transactions(conn, num_records):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM transactions WHERE transaction_id IN (SELECT transaction_id FROM transactions ORDER BY RANDOM() LIMIT %s)",
            (num_records,),
        )
    conn.commit()


def delete_user_profiles(conn, num_records):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM user_profiles WHERE user_id IN (SELECT user_id FROM user_profiles ORDER BY RANDOM() LIMIT %s)",
            (num_records,),
        )
    conn.commit()


if __name__ == "__main__":
    conn = connect_to_db()
    num_records = int(os.getenv("NUM_RECORDS", 10))
    delete_products(conn, num_records)
    delete_transactions(conn, num_records)
    delete_user_profiles(conn, num_records)
    conn.close()
    logging.info(
        f"Deleted {num_records} records in each table: products, user_profiles, and transactions."
    )
