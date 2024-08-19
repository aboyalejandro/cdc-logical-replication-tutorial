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


def insert_product(conn, num_records):
    with conn.cursor() as cur:
        for _ in range(num_records):
            cur.execute(
                """
                INSERT INTO products (product_id, product_name, category, price, stock, description, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    f"PROD-{random.randint(1000, 9999)}",
                    f"Product {random.randint(1, 100)}",
                    random.choice(["Electronics", "Clothing", "Books", "Food"]),
                    random.uniform(10, 1000),
                    random.randint(0, 1000),
                    "Product description",
                    datetime.now(),
                    datetime.now(),
                ),
            )
    conn.commit()


def insert_transaction(conn, num_records):
    with conn.cursor() as cur:
        for _ in range(num_records):
            cur.execute(
                """
                INSERT INTO transactions (transaction_id, user_id, product_id, amount, transaction_type, date, description, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    f"TRX-{random.randint(10000, 99999)}",
                    f"USER-{random.randint(1000, 9999)}",
                    f"PROD-{random.randint(1000, 9999)}",
                    random.uniform(10, 1000),
                    random.choice(["Purchase", "Refund"]),
                    datetime.now() - timedelta(days=random.randint(0, 365)),
                    "Transaction description",
                    datetime.now(),
                ),
            )
    conn.commit()


def insert_user_profile(conn, num_records):
    with conn.cursor() as cur:
        for _ in range(num_records):
            cur.execute(
                """
                INSERT INTO user_profiles (user_id, name, username, email, address, phone_number, dob, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    f"USER-{random.randint(1000, 9999)}",
                    f"User {random.randint(1, 100)}",
                    f"user{random.randint(100, 999)}",
                    f"user{random.randint(100, 999)}@example.com",
                    "123 Main St, City, Country",
                    f"+1-555-{random.randint(1000000, 9999999)}",
                    datetime.now() - timedelta(days=random.randint(365 * 18, 365 * 80)),
                    datetime.now(),
                    datetime.now(),
                ),
            )
    conn.commit()


if __name__ == "__main__":
    conn = connect_to_db()
    num_records = int(os.getenv("NUM_RECORDS", 10))
    insert_product(conn, num_records)
    insert_transaction(conn, num_records)
    insert_user_profile(conn, num_records)
    conn.close()
    logging.info(
        f"Inserted {num_records} records in each table: products, user_profiles, and transactions."
    )
