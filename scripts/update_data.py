import psycopg2
import os
import random
from datetime import datetime, timedelta
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


def update_product(conn, num_records):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT product_id FROM products ORDER BY RANDOM() LIMIT %s", (num_records,)
        )
        product_ids = cur.fetchall()
        for product_id in product_ids:
            cur.execute(
                """
                UPDATE products
                SET price = %s, stock = %s, updated_at = NOW()
                WHERE product_id = %s
            """,
                (random.uniform(10, 1000), random.randint(0, 1000), product_id[0]),
            )
    conn.commit()
    logging.info(f"Updated {num_records} records in products table.")


def update_user_profile(conn, num_records):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT user_id FROM user_profiles ORDER BY RANDOM() LIMIT %s",
            (num_records,),
        )
        user_ids = cur.fetchall()
        for user_id in user_ids:
            cur.execute(
                """
                UPDATE user_profiles
                SET address = %s, phone_number = %s, updated_at = NOW()
                WHERE user_id = %s
            """,
                (
                    f"{random.randint(1, 999)} New St, City, Country",
                    f"+1-555-{random.randint(1000000, 9999999)}",
                    user_id[0],
                ),
            )
    conn.commit()
    logging.info(f"Updated {num_records} records in user_profiles table.")


def update_transaction(conn, num_records):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT transaction_id FROM transactions ORDER BY RANDOM() LIMIT %s",
            (num_records,),
        )
        transaction_ids = cur.fetchall()
        for transaction_id in transaction_ids:
            cur.execute(
                """
                UPDATE transactions
                SET amount = %s, transaction_type = %s, date = %s, description = %s, updated_at = NOW()
                WHERE transaction_id = %s
            """,
                (
                    random.uniform(10, 1000),
                    random.choice(["Purchase", "Refund", "Exchange", "Credit"]),
                    datetime.now() - timedelta(days=random.randint(0, 30)),
                    f"Updated transaction description {random.randint(1, 1000)}",
                    transaction_id[0],
                ),
            )
    conn.commit()
    logging.info(f"Updated {num_records} records in transactions table.")


if __name__ == "__main__":
    conn = connect_to_db()
    num_records = int(os.getenv("NUM_RECORDS", 10))
    update_product(conn, random.randint(1, num_records))
    update_user_profile(conn, random.randint(1, num_records))
    update_transaction(conn, random.randint(1, num_records))
    conn.close()
