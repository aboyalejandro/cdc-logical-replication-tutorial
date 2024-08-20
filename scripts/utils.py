import psycopg2
import os
import logging
from dotenv import load_dotenv


def connect_to_db():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_SOURCE_DB_NAME"),
        user=os.getenv("POSTGRES_SOURCE_USER"),
        password=os.getenv("POSTGRES_SOURCE_PASSWORD"),
        host=os.getenv("POSTGRES_SOURCE_HOST"),
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
