import psycopg2
import os
import logging
import random
from dotenv import load_dotenv
from utils import connect_to_db
from utils import logging_setup

load_dotenv()
logging_setup()


def delete_products(conn, num_records):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM products WHERE product_id IN (SELECT product_id FROM products ORDER BY RANDOM() LIMIT %s)",
            (num_records,),
        )
    conn.commit()
    logging.info(f"Deleted {num_records} records in products table.")


def delete_transactions(conn, num_records):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM transactions WHERE transaction_id IN (SELECT transaction_id FROM transactions ORDER BY RANDOM() LIMIT %s)",
            (num_records,),
        )
    conn.commit()
    logging.info(f"Deleted {num_records} records in transactions table.")


def delete_user_profiles(conn, num_records):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM user_profiles WHERE user_id IN (SELECT user_id FROM user_profiles ORDER BY RANDOM() LIMIT %s)",
            (num_records,),
        )
    conn.commit()
    logging.info(f"Deleted {num_records} records in user_profiles table.")


if __name__ == "__main__":
    conn = connect_to_db()
    num_records = int(os.getenv("NUM_RECORDS", 10))
    delete_products(conn, random.randint(1, num_records))
    delete_transactions(conn, random.randint(1, num_records))
    delete_user_profiles(conn, random.randint(1, num_records))
    conn.close()
