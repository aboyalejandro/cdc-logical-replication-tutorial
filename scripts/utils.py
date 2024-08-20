import psycopg2
import os
import logging
from dotenv import load_dotenv


def connect_to_db(db: str):
    return psycopg2.connect(
        dbname=os.getenv(f"POSTGRES_{db}_DB_NAME"),
        user=os.getenv(f"POSTGRES_{db}_USER"),
        password=os.getenv(f"POSTGRES_{db}_PASSWORD"),
        host=os.getenv(f"POSTGRES_{db}_HOST"),
        port=5432,
    )


def logging_setup():
    return logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def find_tables():
    return """
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """
