import psycopg2
import os
import random
from faker import Faker
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
from utils import connect_to_db
from utils import logging_setup

load_dotenv()
logging_setup()
fake = Faker()


def insert_product(conn, num_records):
    with conn.cursor() as cur:
        for _ in range(num_records):
            cur.execute(
                """
                INSERT INTO products (product_id, product_name, category, price, stock, description, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    fake.uuid4(),
                    fake.word().capitalize(),
                    random.choice(["Electronics", "Clothing", "Books", "Food"]),
                    random.uniform(10, 1000),
                    random.randint(0, 1000),
                    fake.sentence(nb_words=6),
                    datetime.now(),
                    datetime.now(),
                ),
            )
    conn.commit()
    logging.info(f"Inserted {num_records} records in products table.")


def insert_transaction(conn, num_records):
    with conn.cursor() as cur:
        for _ in range(num_records):
            cur.execute(
                """
                INSERT INTO transactions (transaction_id, user_id, product_id, amount, transaction_type, date, description, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    fake.uuid4(),
                    fake.uuid4(),
                    fake.uuid4(),
                    random.uniform(10, 1000),
                    random.choice(["Credit", "Debit", "Purchase", "Refund"]),
                    datetime.now() - timedelta(days=random.randint(0, 365)),
                    fake.sentence(nb_words=6),
                    datetime.now(),
                ),
            )
    conn.commit()
    logging.info(f"Inserted {num_records} records in transactions table.")


def insert_user_profile(conn, num_records):
    with conn.cursor() as cur:
        for _ in range(num_records):
            cur.execute(
                """
                INSERT INTO user_profiles (user_id, name, username, email, address, phone_number, dob, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    fake.uuid4(),
                    fake.name(),
                    fake.user_name(),
                    fake.email(),
                    fake.address(),
                    fake.phone_number(),
                    datetime.now() - timedelta(days=random.randint(365 * 18, 365 * 80)),
                    datetime.now(),
                    datetime.now(),
                ),
            )
    conn.commit()
    logging.info(f"Inserted {num_records} records in user_profiles table.")


if __name__ == "__main__":
    conn = connect_to_db("SOURCE")
    num_records = int(os.getenv("NUM_RECORDS", 10))
    insert_product(conn, random.randint(1, num_records))
    insert_transaction(conn, random.randint(1, num_records))
    insert_user_profile(conn, random.randint(1, num_records))
    conn.close()
